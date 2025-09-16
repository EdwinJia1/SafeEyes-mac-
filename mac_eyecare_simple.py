#!/usr/bin/env python3
"""
MacOS Eye Care Reminder - Simple Reliable Version
专为macOS设计的简洁可靠护眼提醒
"""

import time
import threading
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime

class EyeCareSettings:
    def __init__(self):
        self.config_file = os.path.expanduser('~/.eyecare_simple_settings.json')
        self.default_settings = {
            'work_time': 1,  # 1 minute for quick testing
            'break_time': 10,  # 10 seconds break
            'language': 'en'
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        try:
            with open(self.config_file, 'r') as f:
                settings = json.load(f)
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

class EyeCareReminder:
    def __init__(self):
        self.settings = EyeCareSettings()
        self.is_running = False
        self.reminder_thread = None
        self.temp_files = []
    
    def create_break_html(self, break_duration):
        """Create beautiful nature-themed break page"""
        
        if self.settings.get('language') == 'zh':
            title = "该休息了！"
            message = "请将视线从屏幕上移开，让眼睛休息一下"
            instruction = "看看远处的蓝天白云，放松你的眼睛"
            close_text = "点击任意键或等待倒计时结束"
        else:
            title = "Time for a break!"
            message = "Look away from your screen and rest your eyes"
            instruction = "Enjoy the beautiful blue sky and clouds, relax your eyes"
            close_text = "Press any key or wait for countdown to end"
        
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(180deg, #87CEEB 0%, #98E4FF 30%, #B8F2FF 70%, #90EE90 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            position: relative;
        }}
        
        /* Clouds */
        .cloud {{
            position: absolute;
            background: rgba(255,255,255,0.8);
            border-radius: 50px;
            opacity: 0.7;
        }}
        .cloud1 {{ width: 200px; height: 60px; top: 20%; left: 10%; animation: drift1 25s infinite linear; }}
        .cloud2 {{ width: 150px; height: 40px; top: 30%; right: 20%; animation: drift2 20s infinite linear; }}
        .cloud3 {{ width: 180px; height: 50px; top: 15%; right: 40%; animation: drift3 30s infinite linear; }}
        
        /* Sun */
        .sun {{
            position: absolute;
            top: 15%;
            right: 10%;
            font-size: 60px;
            animation: glow 4s ease-in-out infinite;
        }}
        
        /* Grass */
        .grass {{
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 30%;
            background: linear-gradient(180deg, #90EE90 0%, #32CD32 50%, #228B22 100%);
        }}
        
        /* Flowers */
        .flowers {{
            position: absolute;
            bottom: 8%;
            left: 15%;
            font-size: 30px;
            animation: sway 3s ease-in-out infinite;
        }}
        
        /* Main content */
        .container {{
            text-align: center;
            background: rgba(255,255,255,0.95);
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            max-width: 600px;
            z-index: 100;
        }}
        
        h1 {{
            font-size: 48px;
            color: #2E8B57;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
        }}
        
        .message {{
            font-size: 24px;
            color: #4682B4;
            margin-bottom: 30px;
            line-height: 1.4;
        }}
        
        .countdown {{
            font-size: 36px;
            color: #FF6B6B;
            margin: 30px 0;
            font-weight: bold;
            background: rgba(255,255,255,0.8);
            padding: 20px;
            border-radius: 10px;
        }}
        
        .instruction {{
            font-size: 18px;
            color: #32CD32;
            background: rgba(144,238,144,0.3);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }}
        
        .eye {{
            font-size: 80px;
            margin-bottom: 20px;
            animation: blink 3s infinite;
        }}
        
        @keyframes drift1 {{
            0% {{ transform: translateX(-50px); }}
            100% {{ transform: translateX(calc(100vw + 50px)); }}
        }}
        @keyframes drift2 {{
            0% {{ transform: translateX(-50px); }}
            100% {{ transform: translateX(calc(100vw + 50px)); }}
        }}
        @keyframes drift3 {{
            0% {{ transform: translateX(-50px); }}
            100% {{ transform: translateX(calc(100vw + 50px)); }}
        }}
        @keyframes glow {{
            0%, 100% {{ opacity: 0.8; transform: scale(1); }}
            50% {{ opacity: 1; transform: scale(1.1); }}
        }}
        @keyframes sway {{
            0%, 100% {{ transform: rotate(-5deg); }}
            50% {{ transform: rotate(5deg); }}
        }}
        @keyframes blink {{
            0%, 90%, 100% {{ opacity: 1; }}
            95% {{ opacity: 0.3; }}
        }}
    </style>
</head>
<body>
    <div class="cloud cloud1"></div>
    <div class="cloud cloud2"></div>
    <div class="cloud cloud3"></div>
    <div class="sun">☀️</div>
    <div class="grass"></div>
    <div class="flowers">🌸🌼🌻</div>
    
    <div class="container">
        <div class="eye">👁️</div>
        <h1>{title}</h1>
        <div class="message">{message}</div>
        <div class="countdown" id="countdown">Time remaining: {break_duration} seconds</div>
        <div class="instruction">{instruction}</div>
        <div style="margin-top: 20px; font-size: 14px; color: #666;">{close_text}</div>
    </div>

    <script>
        let timeLeft = {break_duration};
        
        function updateCountdown() {{
            const element = document.getElementById('countdown');
            if (timeLeft > 0) {{
                element.textContent = 'Time remaining: ' + timeLeft + ' seconds';
                timeLeft--;
                setTimeout(updateCountdown, 1000);
            }} else {{
                element.textContent = 'Break is over - back to work!';
                element.style.color = '#32CD32';
                setTimeout(function() {{
                    window.close();
                }}, 2000);
            }}
        }}
        
        // Start countdown
        updateCountdown();
        
        // Close on any key press
        document.addEventListener('keydown', function() {{
            window.close();
        }});
        
        // Close on click
        document.addEventListener('click', function() {{
            window.close();
        }});
        
        // Auto focus
        window.focus();
    </script>
</body>
</html>'''
        
        return html_content
    
    def show_break_reminder(self, break_duration):
        """Show the break reminder"""
        try:
            # Create HTML content
            html_content = self.create_break_html(break_duration)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(html_content)
                html_file = f.name
            
            self.temp_files.append(html_file)
            print(f"📁 Created HTML file: {html_file}")
            
            # Open with Safari
            result = subprocess.run([
                'open', '-a', 'Safari', html_file
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("🌐 Safari opened successfully")
                return True
            else:
                print(f"❌ Safari failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error showing reminder: {e}")
            return False
    
    def start_reminder(self):
        """Start the reminder"""
        if self.is_running:
            print("Reminder is already running")
            return
        
        self.is_running = True
        print("🔥 Eye care reminder started!")
        print(f"Work time: {self.settings.get('work_time')} minutes")
        print(f"Break time: {self.settings.get('break_time')} seconds")
        print("Press Ctrl+C to stop")
        
        self.reminder_thread = threading.Thread(target=self._reminder_loop, daemon=True)
        self.reminder_thread.start()
    
    def stop_reminder(self):
        """Stop the reminder"""
        self.is_running = False
        print("🛑 Eye care reminder stopped")
        
        # Clean up temp files
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
            work_seconds = self.settings.get('work_time') * 60
            
            print(f"⏰ Work period started ({self.settings.get('work_time')} minutes)")
            
            for remaining in range(work_seconds, 0, -1):
                if not self.is_running:
                    return
                time.sleep(1)
                
                # Show countdown every 30 seconds
                if remaining % 30 == 0:
                    minutes_left = remaining // 60
                    print(f"⏱️  Next break in {minutes_left} minutes")
            
            if not self.is_running:
                return
            
            # Break time
            break_duration = self.settings.get('break_time')
            print(f"🌤️  Break time! ({break_duration} seconds)")
            
            # Show fullscreen reminder
            self.show_break_reminder(break_duration)
            
            # Wait for break duration
            time.sleep(break_duration)
            
            print("✅ Break completed")
    
    def configure(self):
        """Configure settings"""
        print("⚙️  Configure Settings")
        try:
            work = input(f"Work time in minutes (current: {self.settings.get('work_time')}): ").strip()
            if work:
                self.settings.set('work_time', int(work))
            
            rest = input(f"Break time in seconds (current: {self.settings.get('break_time')}): ").strip()
            if rest:
                self.settings.set('break_time', int(rest))
            
            lang = input(f"Language [en/zh] (current: {self.settings.get('language')}): ").strip()
            if lang in ['en', 'zh']:
                self.settings.set('language', lang)
            
            print("✅ Settings saved!")
            
        except (ValueError, KeyboardInterrupt):
            print("Settings not changed")
    
    def test_reminder(self):
        """Test the reminder"""
        print("🧪 Testing reminder (5 seconds)...")
        self.show_break_reminder(5)
    
    def run(self):
        """Run interactive interface"""
        while True:
            print("\n🌤️  Eye Care Reminder")
            print("1. Start reminder")
            print("2. Stop reminder") 
            print("3. Test reminder")
            print("4. Configure settings")
            print("5. Quit")
            
            try:
                choice = input("\nSelect (1-5): ").strip()
                
                if choice == '1':
                    self.start_reminder()
                    try:
                        while self.is_running:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        self.stop_reminder()
                
                elif choice == '2':
                    self.stop_reminder()
                
                elif choice == '3':
                    self.test_reminder()
                
                elif choice == '4':
                    self.configure()
                
                elif choice == '5':
                    self.stop_reminder()
                    print("👋 Goodbye!")
                    break
                
                else:
                    print("Invalid choice")
                    
            except KeyboardInterrupt:
                self.stop_reminder()
                print("\n👋 Goodbye!")
                break
            except EOFError:
                break

def main():
    app = EyeCareReminder()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            app.test_reminder()
        elif sys.argv[1] == '--start':
            app.start_reminder()
            try:
                while app.is_running:
                    time.sleep(1)
            except KeyboardInterrupt:
                app.stop_reminder()
        elif sys.argv[1] == '--config':
            app.configure()
        else:
            print("Usage: python3 mac_eyecare_simple.py [--test|--start|--config]")
    else:
        app.run()

if __name__ == '__main__':
    main()