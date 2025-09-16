#!/usr/bin/env python3
"""
MacOS Eye Care Reminder - Native Version
A bilingual eye protection reminder application for macOS using native notifications
支持中英文的macOS护眼提醒应用（使用原生通知）
"""

import time
import threading
import json
import os
import subprocess
import sys
from datetime import datetime

class EyeCareLanguage:
    """Language system for bilingual support"""
    
    LANGUAGES = {
        'en': {
            'app_title': 'Eye Care Reminder',
            'time_for_break': 'Time for a break!',
            'look_away': 'Look away from your screen and rest your eyes for {} seconds.',
            'long_break_title': 'Time for a long break!',
            'long_break_msg': 'Take a longer break to stretch and walk around for {} minutes.',
            'back_to_work': 'Break time is over - back to work!',
            'starting': 'Eye care reminder started',
            'stopping': 'Eye care reminder stopped',
            'cycle_complete': 'Work cycle {} complete',
            'next_break_in': 'Next break in {} minutes',
            'press_ctrl_c': 'Press Ctrl+C to stop the reminder',
            'work_period': 'Work period: {} minutes',
            'break_period': 'Break period: {} seconds', 
            'long_break_period': 'Long break period: {} minutes',
            'cycles_before_long': 'Long break every {} cycles',
            'settings_saved': 'Settings saved successfully'
        },
        'zh': {
            'app_title': '护眼提醒',
            'time_for_break': '该休息了！',
            'look_away': '请将视线从屏幕上移开，让眼睛休息{}秒。',
            'long_break_title': '该进行长时间休息了！',
            'long_break_msg': '请进行更长时间的休息，站起来走动{}分钟。',
            'back_to_work': '休息结束 - 继续工作！',
            'starting': '护眼提醒已启动',
            'stopping': '护眼提醒已停止',
            'cycle_complete': '工作周期{}已完成',
            'next_break_in': '下次休息还有{}分钟',
            'press_ctrl_c': '按 Ctrl+C 停止提醒',
            'work_period': '工作时间：{}分钟',
            'break_period': '休息时间：{}秒',
            'long_break_period': '长休息时间：{}分钟',
            'cycles_before_long': '每{}个周期进行长休息',
            'settings_saved': '设置保存成功'
        }
    }
    
    def __init__(self, language='en'):
        self.current_lang = language
    
    def get(self, key, *args):
        text = self.LANGUAGES[self.current_lang].get(key, key)
        if args:
            return text.format(*args)
        return text
    
    def set_language(self, lang):
        if lang in self.LANGUAGES:
            self.current_lang = lang

class EyeCareSettings:
    """Settings management"""
    
    def __init__(self):
        self.config_file = os.path.expanduser('~/.eyecare_settings.json')
        self.default_settings = {
            'work_time': 20,  # 20 minutes work
            'break_time': 20,  # 20 seconds break
            'long_break_time': 5,  # 5 minute long break
            'cycles_before_long_break': 3,  # Long break every 3 cycles
            'language': 'en',
            'notifications_enabled': True,
            'sound_enabled': True
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        try:
            with open(self.config_file, 'r') as f:
                settings = json.load(f)
                # Ensure all default keys exist
                for key, value in self.default_settings.items():
                    if key not in settings:
                        settings[key] = value
                return settings
        except (FileNotFoundError, json.JSONDecodeError):
            return self.default_settings.copy()
    
    def save_settings(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get(self, key):
        return self.settings.get(key, self.default_settings.get(key))
    
    def set(self, key, value):
        self.settings[key] = value
        return self.save_settings()

class MacNotificationManager:
    """macOS native notification manager"""
    
    @staticmethod
    def send_notification(title, message, sound=True):
        """Send macOS notification"""
        try:
            cmd = [
                'osascript', '-e', 
                f'display notification "{message}" with title "{title}"'
            ]
            if sound:
                cmd = [
                    'osascript', '-e',
                    f'display notification "{message}" with title "{title}" sound name "Glass"'
                ]
            
            subprocess.run(cmd, check=False, capture_output=True)
            return True
        except Exception as e:
            print(f"Failed to send notification: {e}")
            return False
    
    @staticmethod
    def show_dialog(title, message, buttons=["OK"]):
        """Show macOS dialog"""
        try:
            button_list = '", "'.join(buttons)
            script = f'''
            display dialog "{message}" with title "{title}" buttons {{"{button_list}"}} default button 1 with icon note
            '''
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True, check=False)
            return result.returncode == 0
        except Exception as e:
            print(f"Failed to show dialog: {e}")
            return False

class EyeCareReminder:
    """Main eye care reminder application"""
    
    def __init__(self):
        self.settings = EyeCareSettings()
        self.lang = EyeCareLanguage(self.settings.get('language'))
        self.notification_manager = MacNotificationManager()
        
        self.is_running = False
        self.current_cycle = 0
        self.reminder_thread = None
    
    def print_status(self, message):
        """Print status with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {message}")
    
    def show_settings(self):
        """Display current settings"""
        print(f"\n=== {self.lang.get('app_title')} ===")
        print(f"{self.lang.get('work_period', self.settings.get('work_time'))}")
        print(f"{self.lang.get('break_period', self.settings.get('break_time'))}")
        print(f"{self.lang.get('long_break_period', self.settings.get('long_break_time'))}")
        print(f"{self.lang.get('cycles_before_long', self.settings.get('cycles_before_long_break'))}")
        print(f"Language: {self.settings.get('language')}")
        print("=" * 30)
    
    def configure_settings(self):
        """Interactive settings configuration"""
        print(f"\n=== Settings Configuration ===")
        try:
            work_time = input(f"Work time in minutes (current: {self.settings.get('work_time')}): ").strip()
            if work_time:
                self.settings.set('work_time', int(work_time))
            
            break_time = input(f"Break time in seconds (current: {self.settings.get('break_time')}): ").strip()
            if break_time:
                self.settings.set('break_time', int(break_time))
            
            long_break_time = input(f"Long break time in minutes (current: {self.settings.get('long_break_time')}): ").strip()
            if long_break_time:
                self.settings.set('long_break_time', int(long_break_time))
            
            cycles = input(f"Cycles before long break (current: {self.settings.get('cycles_before_long_break')}): ").strip()
            if cycles:
                self.settings.set('cycles_before_long_break', int(cycles))
            
            language = input(f"Language [en/zh] (current: {self.settings.get('language')}): ").strip().lower()
            if language in ['en', 'zh']:
                self.settings.set('language', language)
                self.lang.set_language(language)
            
            print(f"\n{self.lang.get('settings_saved')}")
            
        except ValueError:
            print("Invalid input. Settings not changed.")
        except KeyboardInterrupt:
            print("\nSettings configuration cancelled.")
    
    def start_reminder(self):
        """Start the eye care reminder"""
        if self.is_running:
            return
        
        self.is_running = True
        self.current_cycle = 0
        self.print_status(self.lang.get('starting'))
        self.print_status(self.lang.get('press_ctrl_c'))
        
        # Send initial notification
        self.notification_manager.send_notification(
            self.lang.get('app_title'),
            self.lang.get('starting'),
            self.settings.get('sound_enabled')
        )
        
        self.reminder_thread = threading.Thread(target=self._reminder_loop, daemon=True)
        self.reminder_thread.start()
    
    def stop_reminder(self):
        """Stop the eye care reminder"""
        if not self.is_running:
            return
        
        self.is_running = False
        self.print_status(self.lang.get('stopping'))
        
        # Send stop notification
        self.notification_manager.send_notification(
            self.lang.get('app_title'),
            self.lang.get('stopping'),
            self.settings.get('sound_enabled')
        )
    
    def _reminder_loop(self):
        """Main reminder loop"""
        while self.is_running:
            # Work period
            work_time = self.settings.get('work_time') * 60  # Convert to seconds
            
            # Countdown with periodic updates
            for remaining in range(work_time, 0, -60):  # Update every minute
                if not self.is_running:
                    return
                
                minutes_left = remaining // 60
                if minutes_left > 0 and minutes_left % 5 == 0:  # Update every 5 minutes
                    self.print_status(self.lang.get('next_break_in', minutes_left))
                
                # Sleep for 1 minute or until stop
                for _ in range(60):
                    if not self.is_running:
                        return
                    time.sleep(1)
            
            if not self.is_running:
                return
            
            # Break time
            self.current_cycle += 1
            cycles_before_long = self.settings.get('cycles_before_long_break')
            is_long_break = (self.current_cycle % cycles_before_long == 0)
            
            if is_long_break:
                self._long_break()
            else:
                self._short_break()
            
            self.print_status(self.lang.get('cycle_complete', self.current_cycle))
    
    def _short_break(self):
        """Handle short break"""
        break_duration = self.settings.get('break_time')
        
        title = self.lang.get('time_for_break')
        message = self.lang.get('look_away', break_duration)
        
        self.print_status(f"{title} - {message}")
        
        # Send notification
        self.notification_manager.send_notification(
            title, message, self.settings.get('sound_enabled')
        )
        
        # Show dialog for break
        self.notification_manager.show_dialog(title, message, ["OK"])
        
        # Wait for break duration
        time.sleep(break_duration)
        
        # Break end notification
        back_to_work = self.lang.get('back_to_work')
        self.print_status(back_to_work)
        self.notification_manager.send_notification(
            self.lang.get('app_title'),
            back_to_work,
            self.settings.get('sound_enabled')
        )
    
    def _long_break(self):
        """Handle long break"""
        break_duration = self.settings.get('long_break_time')
        
        title = self.lang.get('long_break_title')
        message = self.lang.get('long_break_msg', break_duration)
        
        self.print_status(f"{title} - {message}")
        
        # Send notification
        self.notification_manager.send_notification(
            title, message, self.settings.get('sound_enabled')
        )
        
        # Show dialog for break
        self.notification_manager.show_dialog(title, message, ["OK"])
        
        # Wait for break duration (in minutes)
        break_seconds = break_duration * 60
        for remaining in range(break_seconds, 0, -60):
            if not self.is_running:
                return
            
            minutes_left = remaining // 60
            if minutes_left > 0 and minutes_left % 2 == 0:
                self.print_status(f"Long break: {minutes_left} minutes remaining")
            
            # Sleep for 1 minute or until stop
            for _ in range(60):
                if not self.is_running:
                    return
                time.sleep(1)
        
        # Break end notification
        back_to_work = self.lang.get('back_to_work')
        self.print_status(back_to_work)
        self.notification_manager.send_notification(
            self.lang.get('app_title'),
            back_to_work,
            self.settings.get('sound_enabled')
        )
    
    def run_interactive(self):
        """Run interactive command-line interface"""
        while True:
            print(f"\n=== {self.lang.get('app_title')} ===")
            print("1. Start reminder")
            print("2. Stop reminder") 
            print("3. Show settings")
            print("4. Configure settings")
            print("5. Switch language")
            print("6. Quit")
            
            try:
                choice = input("\nSelect option (1-6): ").strip()
                
                if choice == '1':
                    if not self.is_running:
                        self.start_reminder()
                        # Keep running until interrupted
                        try:
                            while self.is_running:
                                time.sleep(1)
                        except KeyboardInterrupt:
                            self.stop_reminder()
                    else:
                        print("Reminder is already running")
                
                elif choice == '2':
                    self.stop_reminder()
                
                elif choice == '3':
                    self.show_settings()
                
                elif choice == '4':
                    self.configure_settings()
                
                elif choice == '5':
                    current_lang = self.settings.get('language')
                    new_lang = 'zh' if current_lang == 'en' else 'en'
                    self.settings.set('language', new_lang)
                    self.lang.set_language(new_lang)
                    print(f"Language switched to: {new_lang}")
                
                elif choice == '6':
                    self.stop_reminder()
                    print("Goodbye!")
                    break
                
                else:
                    print("Invalid option")
                    
            except KeyboardInterrupt:
                self.stop_reminder()
                print("\nGoodbye!")
                break
            except EOFError:
                break

def main():
    """Main entry point"""
    app = EyeCareReminder()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--start':
            app.show_settings()
            app.start_reminder()
            try:
                while app.is_running:
                    time.sleep(1)
            except KeyboardInterrupt:
                app.stop_reminder()
        elif sys.argv[1] == '--config':
            app.configure_settings()
        elif sys.argv[1] == '--help':
            print("Eye Care Reminder for macOS")
            print("Usage:")
            print("  python3 mac_eyecare_native.py           # Interactive mode")
            print("  python3 mac_eyecare_native.py --start   # Start reminder directly")
            print("  python3 mac_eyecare_native.py --config  # Configure settings")
            print("  python3 mac_eyecare_native.py --help    # Show this help")
        else:
            print("Unknown argument. Use --help for usage information.")
    else:
        # Interactive mode
        app.run_interactive()

if __name__ == '__main__':
    main()