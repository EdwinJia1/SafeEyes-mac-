#!/usr/bin/env python3
"""
MacOS Eye Care Reminder
A bilingual eye protection reminder application for macOS
支持中英文的macOS护眼提醒应用
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import json
import os
import subprocess
from datetime import datetime, timedelta

class EyeCareLanguage:
    """Language system for bilingual support"""
    
    LANGUAGES = {
        'en': {
            'app_title': 'Eye Care Reminder',
            'work_time': 'Work Time (minutes)',
            'break_time': 'Break Time (minutes)', 
            'long_break_time': 'Long Break Time (minutes)',
            'cycles_before_long_break': 'Cycles Before Long Break',
            'start': 'Start',
            'stop': 'Stop',
            'settings': 'Settings',
            'language': 'Language',
            'english': 'English',
            'chinese': '中文',
            'save': 'Save',
            'cancel': 'Cancel',
            'time_for_break': 'Time for a break!',
            'look_away': 'Look away from your screen and rest your eyes.',
            'break_ending_soon': 'Break ending in',
            'seconds': 'seconds',
            'back_to_work': 'Back to work!',
            'long_break_title': 'Time for a long break!',
            'long_break_msg': 'Take a longer break to stretch and walk around.',
            'status_working': 'Working',
            'status_break': 'Break Time',
            'status_stopped': 'Stopped',
            'next_break_in': 'Next break in',
            'minutes': 'minutes',
            'about': 'About',
            'about_text': 'MacOS Eye Care Reminder v1.0\nProtect your eyes with regular breaks',
            'quit': 'Quit'
        },
        'zh': {
            'app_title': '护眼提醒',
            'work_time': '工作时间（分钟）',
            'break_time': '休息时间（分钟）',
            'long_break_time': '长休息时间（分钟）',
            'cycles_before_long_break': '长休息前的周期数',
            'start': '开始',
            'stop': '停止',
            'settings': '设置',
            'language': '语言',
            'english': 'English',
            'chinese': '中文',
            'save': '保存',
            'cancel': '取消',
            'time_for_break': '该休息了！',
            'look_away': '请将视线从屏幕上移开，让眼睛休息一下。',
            'break_ending_soon': '休息即将结束，还有',
            'seconds': '秒',
            'back_to_work': '继续工作！',
            'long_break_title': '该进行长时间休息了！',
            'long_break_msg': '请进行更长时间的休息，站起来走动一下。',
            'status_working': '工作中',
            'status_break': '休息中',
            'status_stopped': '已停止',
            'next_break_in': '下次休息还有',
            'minutes': '分钟',
            'about': '关于',
            'about_text': 'macOS护眼提醒 v1.0\n通过定期休息保护您的眼睛',
            'quit': '退出'
        }
    }
    
    def __init__(self):
        self.current_lang = 'en'
    
    def get(self, key):
        return self.LANGUAGES[self.current_lang].get(key, key)
    
    def set_language(self, lang):
        if lang in self.LANGUAGES:
            self.current_lang = lang

class EyeCareSettings:
    """Settings management"""
    
    def __init__(self):
        self.config_file = os.path.expanduser('~/.eyecare_settings.json')
        self.default_settings = {
            'work_time': 20,  # 20 minutes work
            'break_time': 1,  # 1 minute break  
            'long_break_time': 5,  # 5 minute long break
            'cycles_before_long_break': 4,  # Long break every 4 cycles
            'language': 'en',
            'notifications_enabled': True
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
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key):
        return self.settings.get(key, self.default_settings.get(key))
    
    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()

class BreakWindow:
    """Break reminder window"""
    
    def __init__(self, parent, lang_system, break_duration, is_long_break=False):
        self.parent = parent
        self.lang = lang_system
        self.break_duration = break_duration
        self.is_long_break = is_long_break
        self.remaining_time = break_duration
        
        self.window = tk.Toplevel()
        self.setup_window()
        self.start_countdown()
    
    def setup_window(self):
        title = self.lang.get('long_break_title') if self.is_long_break else self.lang.get('time_for_break')
        self.window.title(title)
        self.window.geometry('400x200')
        self.window.configure(bg='#2c3e50')
        
        # Make window stay on top
        self.window.attributes('-topmost', True)
        self.window.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Main message
        msg = self.lang.get('long_break_msg') if self.is_long_break else self.lang.get('look_away')
        tk.Label(self.window, text=title, font=('Arial', 16, 'bold'), 
                fg='white', bg='#2c3e50').pack(pady=20)
        
        tk.Label(self.window, text=msg, font=('Arial', 12), 
                fg='white', bg='#2c3e50', wraplength=350).pack(pady=10)
        
        # Countdown display
        self.countdown_label = tk.Label(self.window, text='', font=('Arial', 14, 'bold'), 
                                       fg='#e74c3c', bg='#2c3e50')
        self.countdown_label.pack(pady=10)
        
        # Skip button
        tk.Button(self.window, text=self.lang.get('back_to_work'), 
                 command=self.close_window, bg='#3498db', fg='white', 
                 font=('Arial', 12), padx=20).pack(pady=10)
    
    def center_window(self):
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (self.window.winfo_width() // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f'+{x}+{y}')
    
    def start_countdown(self):
        self.countdown_thread = threading.Thread(target=self.countdown_worker, daemon=True)
        self.countdown_thread.start()
    
    def countdown_worker(self):
        while self.remaining_time > 0:
            if not self.window.winfo_exists():
                break
                
            try:
                countdown_text = f"{self.lang.get('break_ending_soon')} {self.remaining_time} {self.lang.get('seconds')}"
                self.window.after(0, lambda: self.countdown_label.config(text=countdown_text))
                time.sleep(1)
                self.remaining_time -= 1
            except:
                break
        
        if self.remaining_time <= 0:
            self.window.after(0, self.close_window)
    
    def close_window(self):
        try:
            self.window.destroy()
        except:
            pass

class EyeCareApp:
    """Main application class"""
    
    def __init__(self):
        self.settings = EyeCareSettings()
        self.lang = EyeCareLanguage()
        self.lang.set_language(self.settings.get('language'))
        
        self.is_running = False
        self.current_cycle = 0
        self.work_thread = None
        
        self.setup_ui()
        self.update_status()
    
    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title(self.lang.get('app_title'))
        self.root.geometry('350x300')
        self.root.resizable(False, False)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status display
        self.status_var = tk.StringVar()
        self.status_var.set(self.lang.get('status_stopped'))
        ttk.Label(main_frame, textvariable=self.status_var, font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Next break info
        self.next_break_var = tk.StringVar()
        self.next_break_var.set('')
        ttk.Label(main_frame, textvariable=self.next_break_var, font=('Arial', 10)).grid(row=1, column=0, columnspan=2, pady=5)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.start_button = ttk.Button(button_frame, text=self.lang.get('start'), command=self.toggle_timer)
        self.start_button.grid(row=0, column=0, padx=5)
        
        ttk.Button(button_frame, text=self.lang.get('settings'), command=self.show_settings).grid(row=0, column=1, padx=5)
        
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        app_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang.get('app_title'), menu=app_menu)
        app_menu.add_command(label=self.lang.get('about'), command=self.show_about)
        app_menu.add_separator()
        app_menu.add_command(label=self.lang.get('quit'), command=self.quit_app)
    
    def toggle_timer(self):
        if self.is_running:
            self.stop_timer()
        else:
            self.start_timer()
    
    def start_timer(self):
        self.is_running = True
        self.current_cycle = 0
        self.start_button.config(text=self.lang.get('stop'))
        self.work_thread = threading.Thread(target=self.work_cycle, daemon=True)
        self.work_thread.start()
    
    def stop_timer(self):
        self.is_running = False
        self.start_button.config(text=self.lang.get('start'))
        self.status_var.set(self.lang.get('status_stopped'))
        self.next_break_var.set('')
    
    def work_cycle(self):
        while self.is_running:
            # Work period
            work_time = self.settings.get('work_time') * 60  # Convert to seconds
            self.root.after(0, lambda: self.status_var.set(self.lang.get('status_working')))
            
            for remaining in range(work_time, 0, -1):
                if not self.is_running:
                    return
                
                minutes_left = remaining // 60
                self.root.after(0, lambda m=minutes_left: self.next_break_var.set(
                    f"{self.lang.get('next_break_in')} {m} {self.lang.get('minutes')}"))
                time.sleep(1)
            
            if not self.is_running:
                return
            
            # Break time
            self.current_cycle += 1
            cycles_before_long = self.settings.get('cycles_before_long_break')
            is_long_break = (self.current_cycle % cycles_before_long == 0)
            
            if is_long_break:
                break_duration = self.settings.get('long_break_time') * 60
            else:
                break_duration = self.settings.get('break_time') * 60
            
            self.root.after(0, lambda: self.status_var.set(self.lang.get('status_break')))
            self.root.after(0, lambda: self.next_break_var.set(''))
            
            # Show break window
            self.root.after(0, lambda: BreakWindow(self.root, self.lang, break_duration, is_long_break))
            
            # Send macOS notification
            if self.settings.get('notifications_enabled'):
                self.send_notification(is_long_break)
            
            time.sleep(break_duration)
    
    def send_notification(self, is_long_break):
        """Send macOS notification"""
        try:
            title = self.lang.get('long_break_title') if is_long_break else self.lang.get('time_for_break')
            message = self.lang.get('long_break_msg') if is_long_break else self.lang.get('look_away')
            
            subprocess.run([
                'osascript', '-e', 
                f'display notification "{message}" with title "{title}"'
            ], check=False)
        except Exception as e:
            print(f"Failed to send notification: {e}")
    
    def show_settings(self):
        SettingsWindow(self.root, self.settings, self.lang, self.update_language)
    
    def show_about(self):
        messagebox.showinfo(self.lang.get('about'), self.lang.get('about_text'))
    
    def update_language(self):
        """Update UI language"""
        self.lang.set_language(self.settings.get('language'))
        self.root.title(self.lang.get('app_title'))
        self.start_button.config(text=self.lang.get('stop') if self.is_running else self.lang.get('start'))
        self.update_status()
    
    def update_status(self):
        if self.is_running:
            self.status_var.set(self.lang.get('status_working'))
        else:
            self.status_var.set(self.lang.get('status_stopped'))
    
    def quit_app(self):
        self.is_running = False
        self.root.quit()
    
    def run(self):
        self.root.mainloop()

class SettingsWindow:
    """Settings configuration window"""
    
    def __init__(self, parent, settings, lang_system, update_callback):
        self.parent = parent
        self.settings = settings
        self.lang = lang_system
        self.update_callback = update_callback
        
        self.window = tk.Toplevel(parent)
        self.setup_window()
    
    def setup_window(self):
        self.window.title(self.lang.get('settings'))
        self.window.geometry('300x250')
        self.window.resizable(False, False)
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Center window
        self.center_window()
        
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Work time
        ttk.Label(main_frame, text=self.lang.get('work_time')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.work_time_var = tk.StringVar(value=str(self.settings.get('work_time')))
        ttk.Entry(main_frame, textvariable=self.work_time_var, width=10).grid(row=0, column=1, pady=5)
        
        # Break time
        ttk.Label(main_frame, text=self.lang.get('break_time')).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.break_time_var = tk.StringVar(value=str(self.settings.get('break_time')))
        ttk.Entry(main_frame, textvariable=self.break_time_var, width=10).grid(row=1, column=1, pady=5)
        
        # Long break time
        ttk.Label(main_frame, text=self.lang.get('long_break_time')).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.long_break_time_var = tk.StringVar(value=str(self.settings.get('long_break_time')))
        ttk.Entry(main_frame, textvariable=self.long_break_time_var, width=10).grid(row=2, column=1, pady=5)
        
        # Cycles before long break
        ttk.Label(main_frame, text=self.lang.get('cycles_before_long_break')).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cycles_var = tk.StringVar(value=str(self.settings.get('cycles_before_long_break')))
        ttk.Entry(main_frame, textvariable=self.cycles_var, width=10).grid(row=3, column=1, pady=5)
        
        # Language selection
        ttk.Label(main_frame, text=self.lang.get('language')).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.language_var = tk.StringVar(value=self.settings.get('language'))
        language_combo = ttk.Combobox(main_frame, textvariable=self.language_var, values=['en', 'zh'], width=8, state='readonly')
        language_combo.grid(row=4, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text=self.lang.get('save'), command=self.save_settings).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text=self.lang.get('cancel'), command=self.window.destroy).grid(row=0, column=1, padx=5)
    
    def center_window(self):
        self.window.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.window.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f'+{x}+{y}')
    
    def save_settings(self):
        try:
            # Validate and save settings
            work_time = int(self.work_time_var.get())
            break_time = int(self.break_time_var.get())
            long_break_time = int(self.long_break_time_var.get())
            cycles = int(self.cycles_var.get())
            language = self.language_var.get()
            
            if work_time <= 0 or break_time <= 0 or long_break_time <= 0 or cycles <= 0:
                raise ValueError("All values must be positive")
            
            self.settings.set('work_time', work_time)
            self.settings.set('break_time', break_time)
            self.settings.set('long_break_time', long_break_time)
            self.settings.set('cycles_before_long_break', cycles)
            self.settings.set('language', language)
            
            self.update_callback()
            self.window.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid positive numbers")

if __name__ == '__main__':
    app = EyeCareApp()
    app.run()