#!/usr/bin/env python3
"""
MacOS Eye Care Reminder - Fullscreen Version
A bilingual eye protection reminder with fullscreen interruption for macOS
支持全屏提醒的macOS护眼提醒应用
"""

import time
import threading
import json
import os
import subprocess
import sys
import tempfile
import webbrowser
from datetime import datetime

class EyeCareLanguage:
    """Language system for bilingual support"""
    
    LANGUAGES = {
        'en': {
            'app_title': 'Eye Care Reminder',
            'time_for_break': 'Time for a break!',
            'look_away': 'Look away from your screen and rest your eyes.',
            'break_instructions': 'Follow the 20-20-20 rule:\\n• Look at something 20 feet away\\n• For at least 20 seconds\\n• Blink frequently to moisten your eyes',
            'long_break_title': 'Time for a long break!',
            'long_break_msg': 'Stand up, stretch, and walk around.',
            'long_break_instructions': 'Take a longer break to:\\n• Stand up and stretch your body\\n• Walk around for better circulation\\n• Do some neck and shoulder exercises\\n• Hydrate yourself',
            'back_to_work': 'Break time is over - back to work!',
            'starting': 'Eye care reminder started with FULLSCREEN mode',
            'stopping': 'Eye care reminder stopped',
            'cycle_complete': 'Work cycle {} complete',
            'next_break_in': 'Next break in {} minutes',
            'press_ctrl_c': 'Press Ctrl+C to stop the reminder',
            'work_period': 'Work period: {} minutes',
            'break_period': 'Break period: {} seconds', 
            'long_break_period': 'Long break period: {} minutes',
            'cycles_before_long': 'Long break every {} cycles',
            'settings_saved': 'Settings saved successfully',
            'fullscreen_mode': 'Fullscreen reminder mode',
            'reminder_modes': 'Reminder modes: 1=Dialog, 2=Fullscreen HTML, 3=Large Dialog',
            'countdown': 'Time remaining: {} seconds',
            'close_break': 'Click OK or press Enter when ready to continue',
            'eye_exercises': 'Eye Exercises',
            'exercise_1': '1. Close your eyes tightly for 2 seconds',
            'exercise_2': '2. Look up, down, left, right (2 seconds each)',
            'exercise_3': '3. Roll your eyes clockwise, then counterclockwise',
            'exercise_4': '4. Focus on near object, then far object',
            'breathe_deeply': 'Remember to breathe deeply and relax'
        },
        'zh': {
            'app_title': '护眼提醒',
            'time_for_break': '该休息了！',
            'look_away': '请将视线从屏幕上移开，让眼睛休息。',
            'break_instructions': '遵循20-20-20法则：\\n• 看20英尺外的物体\\n• 至少看20秒\\n• 频繁眨眼保持眼部湿润',
            'long_break_title': '该进行长时间休息了！',
            'long_break_msg': '请站起来，伸展身体，四处走动。',
            'long_break_instructions': '进行长时间休息：\\n• 站起来伸展身体\\n• 四处走动促进血液循环\\n• 做一些颈部和肩部运动\\n• 适当补充水分',
            'back_to_work': '休息结束 - 继续工作！',
            'starting': '护眼提醒已启动（全屏模式）',
            'stopping': '护眼提醒已停止',
            'cycle_complete': '工作周期{}已完成',
            'next_break_in': '下次休息还有{}分钟',
            'press_ctrl_c': '按 Ctrl+C 停止提醒',
            'work_period': '工作时间：{}分钟',
            'break_period': '休息时间：{}秒',
            'long_break_period': '长休息时间：{}分钟',
            'cycles_before_long': '每{}个周期进行长休息',
            'settings_saved': '设置保存成功',
            'fullscreen_mode': '全屏提醒模式',
            'reminder_modes': '提醒模式：1=对话框，2=全屏HTML，3=大对话框',
            'countdown': '剩余时间：{}秒',
            'close_break': '准备好继续工作时点击确定或按回车',
            'eye_exercises': '眼部运动',
            'exercise_1': '1. 紧闭双眼2秒',
            'exercise_2': '2. 向上、下、左、右看（各2秒）',
            'exercise_3': '3. 顺时针转动眼球，再逆时针转动',
            'exercise_4': '4. 先看近物，再看远物',
            'breathe_deeply': '记住要深呼吸并放松'
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
        self.config_file = os.path.expanduser('~/.eyecare_fullscreen_settings.json')
        self.default_settings = {
            'work_time': 20,  # 20 minutes work
            'break_time': 20,  # 20 seconds break
            'long_break_time': 5,  # 5 minute long break
            'cycles_before_long_break': 3,  # Long break every 3 cycles
            'language': 'en',
            'notifications_enabled': True,
            'sound_enabled': True,
            'reminder_mode': 2  # 1=dialog, 2=fullscreen_html, 3=large_dialog
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

class FullscreenReminderManager:
    """Fullscreen reminder display manager"""
    
    @staticmethod
    def create_html_reminder(lang_system, break_duration, is_long_break=False):
        """Create fullscreen HTML reminder"""
        
        title = lang_system.get('long_break_title') if is_long_break else lang_system.get('time_for_break')
        instructions = lang_system.get('long_break_instructions') if is_long_break else lang_system.get('break_instructions')
        
        html_content = f"""
<!DOCTYPE html>
<html lang="{lang_system.current_lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: linear-gradient(180deg, #87CEEB 0%, #98E4FF 40%, #B8F2FF 60%, #90EE90 100%);
            position: relative;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }}
        
        /* Sky background with fluffy clouds */
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 70%;
            background: 
                radial-gradient(ellipse 300px 100px at 20% 30%, rgba(255,255,255,0.9) 40%, transparent 60%),
                radial-gradient(ellipse 400px 120px at 70% 25%, rgba(255,255,255,0.7) 40%, transparent 60%),
                radial-gradient(ellipse 250px 80px at 85% 40%, rgba(255,255,255,0.8) 40%, transparent 60%),
                radial-gradient(ellipse 350px 90px at 10% 60%, rgba(255,255,255,0.6) 40%, transparent 60%),
                radial-gradient(ellipse 200px 60px at 60% 15%, rgba(255,255,255,0.7) 40%, transparent 60%);
            z-index: -2;
            animation: cloud-drift 20s ease-in-out infinite;
        }}
        
        /* Grass at bottom */
        body::after {{
            content: '';
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 35%;
            background: linear-gradient(180deg, #90EE90 0%, #32CD32 40%, #228B22 100%);
            z-index: -1;
        }}
        
        .reminder-container {{
            text-align: center;
            max-width: 800px;
            padding: 60px 40px;
            background: rgba(255, 255, 255, 0.92);
            border-radius: 25px;
            backdrop-filter: blur(15px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1), 0 5px 15px rgba(0, 0, 0, 0.07);
            border: 2px solid rgba(255, 255, 255, 0.6);
            color: #2F4F4F;
            position: relative;
            z-index: 10;
        }}
        
        .title {{
            font-size: 4rem;
            font-weight: 700;
            margin-bottom: 30px;
            color: #2E8B57;
            text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.8);
            animation: gentle-pulse 3s infinite;
        }}
        
        .subtitle {{
            font-size: 1.8rem;
            margin-bottom: 40px;
            color: #4682B4;
            opacity: 0.9;
        }}
        
        .instructions {{
            font-size: 1.3rem;
            line-height: 1.8;
            margin-bottom: 40px;
            background: rgba(173, 216, 230, 0.3);
            padding: 30px;
            border-radius: 20px;
            white-space: pre-line;
            color: #2F4F4F;
            border: 1px solid rgba(135, 206, 235, 0.4);
        }}
        
        .countdown {{
            font-size: 3rem;
            font-weight: bold;
            color: #FF6B6B;
            margin-bottom: 30px;
            text-shadow: 1px 1px 3px rgba(255, 255, 255, 0.8);
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 15px;
            display: inline-block;
        }}
        
        .exercises {{
            text-align: left;
            margin: 30px 0;
            background: rgba(152, 251, 152, 0.4);
            padding: 25px;
            border-radius: 20px;
            border: 1px solid rgba(144, 238, 144, 0.6);
        }}
        
        .exercise-title {{
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
            color: #228B22;
        }}
        
        .exercise-item {{
            font-size: 1.1rem;
            margin-bottom: 10px;
            padding: 8px 0;
            color: #2F4F4F;
        }}
        
        .close-instruction {{
            font-size: 1.2rem;
            margin-top: 40px;
            padding: 20px;
            background: rgba(173, 216, 230, 0.4);
            border-radius: 15px;
            color: #4682B4;
            border: 1px solid rgba(135, 206, 235, 0.5);
        }}
        
        .eye-icon {{
            font-size: 5rem;
            margin-bottom: 20px;
            animation: peaceful-blink 4s infinite;
        }}
        
        .nature-icons {{
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 2rem;
            opacity: 0.7;
        }}
        
        .sun {{
            position: fixed;
            top: 10%;
            right: 15%;
            font-size: 4rem;
            color: #FFD700;
            animation: sun-glow 6s infinite;
            z-index: -1;
        }}
        
        .birds {{
            position: fixed;
            top: 25%;
            left: 20%;
            font-size: 1.5rem;
            color: #696969;
            animation: fly 20s infinite linear;
            z-index: -1;
        }}
        
        .flowers {{
            position: fixed;
            bottom: 10%;
            left: 10%;
            font-size: 2rem;
            z-index: -1;
            animation: sway 4s ease-in-out infinite;
        }}
        
        @keyframes gentle-pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.02); }}
        }}
        
        @keyframes peaceful-blink {{
            0%, 85%, 100% {{ opacity: 1; }}
            90%, 95% {{ opacity: 0.2; }}
        }}
        
        @keyframes sun-glow {{
            0%, 100% {{ opacity: 0.8; transform: scale(1); }}
            50% {{ opacity: 1; transform: scale(1.1); }}
        }}
        
        @keyframes fly {{
            0% {{ transform: translateX(-100px); }}
            100% {{ transform: translateX(calc(100vw + 100px)); }}
        }}
        
        @keyframes sway {{
            0%, 100% {{ transform: rotate(-2deg); }}
            50% {{ transform: rotate(2deg); }}
        }}
        
        @keyframes cloud-drift {{
            0%, 100% {{ transform: translateX(0px); }}
            50% {{ transform: translateX(30px); }}
        }}
        
        .breathe {{
            font-size: 1.2rem;
            font-style: italic;
            color: #32CD32;
            margin-top: 20px;
            background: rgba(255, 255, 255, 0.7);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(50, 205, 50, 0.4);
        }}
    </style>
</head>
<body>
    <!-- Natural decoration elements -->
    <div class="sun">☀️</div>
    <div class="birds">🕊️ 🕊️</div>
    <div class="flowers">🌸 🌼 🌻</div>
    
    <div class="reminder-container">
        <div class="eye-icon">👁️</div>
        <h1 class="title">{title}</h1>
        <div class="subtitle">{lang_system.get('look_away')}</div>
        
        <div class="countdown" id="countdown">{lang_system.get('countdown', break_duration)}</div>
        
        <div class="instructions">{instructions.replace('\\n', '<br>')}</div>
        
        <div class="exercises">
            <div class="exercise-title">{lang_system.get('eye_exercises')}</div>
            <div class="exercise-item">{lang_system.get('exercise_1')}</div>
            <div class="exercise-item">{lang_system.get('exercise_2')}</div>
            <div class="exercise-item">{lang_system.get('exercise_3')}</div>
            <div class="exercise-item">{lang_system.get('exercise_4')}</div>
        </div>
        
        <div class="breathe">{lang_system.get('breathe_deeply')}</div>
        
        <div class="close-instruction">{lang_system.get('close_break')}</div>
    </div>

    <script>
        let timeLeft = {break_duration};
        
        function updateCountdown() {{
            const countdownElement = document.getElementById('countdown');
            if (timeLeft > 0) {{
                countdownElement.textContent = 'Time remaining: ' + timeLeft + ' seconds';
                timeLeft--;
                setTimeout(updateCountdown, 1000);
            }} else {{
                countdownElement.textContent = 'Break time is over - back to work!';
                countdownElement.style.color = '#90EE90';
                setTimeout(() => {{
                    window.close();
                }}, 3000);
            }}
        }}
        
        // Start countdown
        updateCountdown();
        
        // Close on keypress
        document.addEventListener('keydown', function(event) {{
            if (event.key === 'Enter' || event.key === 'Escape' || event.key === ' ') {{
                window.close();
            }}
        }});
        
        // Auto-focus for immediate key response
        window.focus();
    </script>
</body>
</html>
        """
        
        return html_content
    
    @staticmethod
    def show_fullscreen_html_reminder(lang_system, break_duration, is_long_break=False):
        """Show fullscreen HTML reminder"""
        try:
            # Create temporary HTML file
            html_content = FullscreenReminderManager.create_html_reminder(
                lang_system, break_duration, is_long_break
            )
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(html_content)
                html_file = f.name
            
            # Open in fullscreen mode with Safari
            subprocess.run([
                'open', '-a', 'Safari', html_file
            ], check=False)
            
            # Alternative: Use default browser
            # webbrowser.open(f'file://{html_file}')
            
            return html_file
            
        except Exception as e:
            print(f"Failed to show fullscreen HTML reminder: {e}")
            return None
    
    @staticmethod
    def show_large_dialog_reminder(lang_system, break_duration, is_long_break=False):
        """Show large modal dialog reminder"""
        try:
            title = lang_system.get('long_break_title') if is_long_break else lang_system.get('time_for_break')
            instructions = lang_system.get('long_break_instructions') if is_long_break else lang_system.get('break_instructions')
            
            message = f"""{lang_system.get('look_away')}

{instructions}

{lang_system.get('countdown', break_duration)}

{lang_system.get('close_break')}"""
            
            script = f'''
            tell application "System Events"
                activate
                set theResult to display dialog "{message}" with title "{title}" with icon note buttons {{"OK"}} default button 1 giving up after {break_duration}
            end tell
            '''
            
            subprocess.run(['osascript', '-e', script], check=False)
            return True
            
        except Exception as e:
            print(f"Failed to show large dialog reminder: {e}")
            return False
    
    @staticmethod
    def show_fullscreen_terminal_reminder(lang_system, break_duration, is_long_break=False):
        """Show fullscreen terminal reminder"""
        try:
            title = lang_system.get('long_break_title') if is_long_break else lang_system.get('time_for_break')
            instructions = lang_system.get('long_break_instructions') if is_long_break else lang_system.get('break_instructions')
            
            # Clear screen and show fullscreen text
            os.system('clear')
            
            print("\n" * 5)
            print("=" * 80)
            print(f"{title:^80}")
            print("=" * 80)
            print()
            print(f"{lang_system.get('look_away'):^80}")
            print()
            print("=" * 80)
            print()
            
            # Instructions
            for line in instructions.split('\\n'):
                print(f"{line:^80}")
            
            print("\n" + "=" * 80)
            print(f"{lang_system.get('close_break'):^80}")
            print("=" * 80)
            
            # Countdown
            for remaining in range(break_duration, 0, -1):
                print(f"\r{lang_system.get('countdown', remaining):^80}", end='', flush=True)
                time.sleep(1)
            
            print(f"\r{lang_system.get('back_to_work'):^80}")
            print("\n" * 3)
            
            return True
            
        except Exception as e:
            print(f"Failed to show terminal reminder: {e}")
            return False

class EyeCareReminder:
    """Main eye care reminder application with fullscreen support"""
    
    def __init__(self):
        self.settings = EyeCareSettings()
        self.lang = EyeCareLanguage(self.settings.get('language'))
        self.reminder_manager = FullscreenReminderManager()
        
        self.is_running = False
        self.current_cycle = 0
        self.reminder_thread = None
        self.temp_files = []
    
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
        print(f"{self.lang.get('fullscreen_mode')}: {self.settings.get('reminder_mode')}")
        print(f"{self.lang.get('reminder_modes')}")
        print("=" * 50)
    
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
            
            reminder_mode = input(f"Reminder mode [1=Dialog, 2=Fullscreen HTML, 3=Large Dialog] (current: {self.settings.get('reminder_mode')}): ").strip()
            if reminder_mode in ['1', '2', '3']:
                self.settings.set('reminder_mode', int(reminder_mode))
            
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
        
        self.reminder_thread = threading.Thread(target=self._reminder_loop, daemon=True)
        self.reminder_thread.start()
    
    def stop_reminder(self):
        """Stop the eye care reminder"""
        if not self.is_running:
            return
        
        self.is_running = False
        self.print_status(self.lang.get('stopping'))
        
        # Cleanup temp files
        for temp_file in self.temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        self.temp_files = []
    
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
            
            self._show_break_reminder(is_long_break)
            self.print_status(self.lang.get('cycle_complete', self.current_cycle))
    
    def _show_break_reminder(self, is_long_break):
        """Show break reminder based on selected mode"""
        if is_long_break:
            break_duration = self.settings.get('long_break_time') * 60
        else:
            break_duration = self.settings.get('break_time')
        
        reminder_mode = self.settings.get('reminder_mode')
        
        if reminder_mode == 1:
            # Standard dialog
            self.reminder_manager.show_large_dialog_reminder(
                self.lang, break_duration, is_long_break
            )
        elif reminder_mode == 2:
            # Fullscreen HTML
            temp_file = self.reminder_manager.show_fullscreen_html_reminder(
                self.lang, break_duration, is_long_break
            )
            if temp_file:
                self.temp_files.append(temp_file)
        elif reminder_mode == 3:
            # Large dialog
            self.reminder_manager.show_large_dialog_reminder(
                self.lang, break_duration, is_long_break
            )
        
        # Wait for break duration
        time.sleep(break_duration)
    
    def run_interactive(self):
        """Run interactive command-line interface"""
        while True:
            print(f"\n=== {self.lang.get('app_title')} ===")
            print("1. Start reminder")
            print("2. Stop reminder") 
            print("3. Show settings")
            print("4. Configure settings")
            print("5. Switch language")
            print("6. Test fullscreen reminder")
            print("7. Quit")
            
            try:
                choice = input("\nSelect option (1-7): ").strip()
                
                if choice == '1':
                    if not self.is_running:
                        self.start_reminder()
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
                    print("Testing fullscreen reminder...")
                    self._show_break_reminder(False)
                
                elif choice == '7':
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
        elif sys.argv[1] == '--test':
            print("Testing fullscreen reminder...")
            app._show_break_reminder(False)
        elif sys.argv[1] == '--help':
            print("Eye Care Reminder with Fullscreen Support for macOS")
            print("Usage:")
            print("  python3 mac_eyecare_fullscreen.py           # Interactive mode")
            print("  python3 mac_eyecare_fullscreen.py --start   # Start reminder directly")
            print("  python3 mac_eyecare_fullscreen.py --config  # Configure settings")
            print("  python3 mac_eyecare_fullscreen.py --test    # Test fullscreen reminder")
            print("  python3 mac_eyecare_fullscreen.py --help    # Show this help")
        else:
            print("Unknown argument. Use --help for usage information.")
    else:
        # Interactive mode
        app.run_interactive()

if __name__ == '__main__':
    main()