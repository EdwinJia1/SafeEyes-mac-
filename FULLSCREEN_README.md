# 🔥 Fullscreen Eye Care Reminder / 全屏护眼提醒

**A POWERFUL bilingual eye protection app with fullscreen interruption for macOS!**

**专为macOS设计的强力双语护眼提醒应用，支持全屏强制休息！**

## 💥 What Makes This Special / 特色功能

Unlike gentle notifications that you can easily ignore, this app **FORCES** you to take breaks with:

与容易忽略的温和通知不同，此应用程序**强制**你休息：

- 🖥️ **Fullscreen HTML Page** - Beautiful, animated break screen
- 📱 **Large System Dialogs** - Hard to miss modal windows  
- 🎯 **Mandatory Interruption** - You MUST acknowledge the break
- 🌏 **Bilingual Support** - English & Chinese (中英文切换)
- ⚙️ **3 Reminder Modes** - Choose your preferred interruption style

## 🚀 Quick Start / 快速开始

### Test the Fullscreen Effect First / 先测试全屏效果
```bash
python3 mac_eyecare_fullscreen.py --test
```

### Start with Interactive Menu / 交互式菜单启动
```bash
python3 mac_eyecare_fullscreen.py
# or 或者
chmod +x start_fullscreen_eyecare.sh && ./start_fullscreen_eyecare.sh
```

### Start Directly / 直接启动
```bash
python3 mac_eyecare_fullscreen.py --start
```

## 🎛️ Reminder Modes / 提醒模式

### Mode 1: Large Dialog / 模式1：大对话框
- System native modal dialog
- Appears in front of all applications
- Auto-closes after break time
- **Best for**: Quick acknowledgment

### Mode 2: Fullscreen HTML (Recommended) / 模式2：全屏HTML（推荐）
- **Beautiful animated webpage**
- **Opens in Safari fullscreen**
- Gradient backgrounds with pulse effects
- Eye exercises and breathing reminders
- Countdown timer with visual effects
- **Best for**: Immersive break experience

### Mode 3: System Modal Dialog / 模式3：系统模态对话框
- Native macOS dialog with timeout
- Blocks other applications
- Simple but effective
- **Best for**: Minimal disruption

## ⚙️ How to Configure / 如何配置

Run the program and select option 4, or use:
```bash
python3 mac_eyecare_fullscreen.py --config
```

### Settings You Can Adjust / 可调整设置:
- **Work Time** / 工作时间: Default 20 minutes / 默认20分钟
- **Break Time** / 休息时间: Default 20 seconds / 默认20秒  
- **Long Break** / 长休息: Default 5 minutes / 默认5分钟
- **Reminder Mode** / 提醒模式: 1, 2, or 3 / 1、2或3
- **Language** / 语言: English or Chinese / 英语或中文

## 🎯 What Happens During a Break / 休息时会发生什么

### Short Break (20 seconds) / 短休息（20秒）
1. **Screen takeover** - Your work is interrupted
2. **Eye exercise instructions** - 20-20-20 rule guidance
3. **Countdown timer** - Shows remaining time
4. **Visual reminders** - Blink, look away, breathe

### Long Break (5 minutes) / 长休息（5分钟）
1. **Full interruption** - Stand up and move
2. **Detailed instructions** - Stretching and walking
3. **Extended timer** - Proper rest duration
4. **Health reminders** - Hydration and circulation

## 🎨 Fullscreen HTML Features / 全屏HTML功能

The **Mode 2** experience includes:

**模式2**体验包括：

- 🎨 **Beautiful Design** - Gradient backgrounds, modern UI
- ✨ **Smooth Animations** - Pulsing text, blinking eye icon
- 📊 **Live Countdown** - Real-time timer updates
- 🧘 **Eye Exercises** - Step-by-step guidance
- 🎹 **Keyboard Control** - Press Enter/Space/Escape to close
- 📱 **Responsive** - Works on any screen size

## 💡 Pro Tips / 专业提示

### For Maximum Effectiveness / 获得最大效果:
1. **Use Mode 2** for the most compelling break experience
2. **Set shorter work periods** initially (10-15 minutes) to build habits
3. **Enable sound** for audio notifications
4. **Don't skip breaks** - the app is designed to force compliance!

### For Different Work Styles / 适应不同工作风格:
- **Intense focus work**: Use Mode 2 with longer work periods
- **Frequent task switching**: Use Mode 1 with shorter breaks
- **Presentation mode**: Temporarily stop the reminder

## 🔧 Advanced Usage / 高级用法

### Command Line Options / 命令行选项:
```bash
python3 mac_eyecare_fullscreen.py --help     # Show help
python3 mac_eyecare_fullscreen.py --start    # Direct start
python3 mac_eyecare_fullscreen.py --config   # Configure settings
python3 mac_eyecare_fullscreen.py --test     # Test reminder
```

### Interactive Menu Options / 交互菜单选项:
1. **Start reminder** - Begin the eye care timer
2. **Stop reminder** - Stop the running timer  
3. **Show settings** - View current configuration
4. **Configure settings** - Modify all settings
5. **Switch language** - Toggle English/Chinese
6. **Test fullscreen** - Preview the break experience
7. **Quit** - Exit application

## 🏥 Health Benefits / 健康益处

This app helps prevent:
此应用帮助预防：

- 👁️ **Digital Eye Strain** / 数字眼疲劳
- 🦴 **Poor Posture** / 不良姿势  
- 🩸 **Poor Circulation** / 血液循环不良
- 🧠 **Mental Fatigue** / 精神疲劳
- 😴 **Sleep Problems** / 睡眠问题

## 🆘 Troubleshooting / 故障排除

### If fullscreen HTML doesn't work / 如果全屏HTML不工作:
1. Check if Safari is your default browser
2. Try Mode 1 or 3 as alternatives
3. Ensure you have internet access

### If dialogs don't appear / 如果对话框不出现:
1. Check System Preferences → Security & Privacy → Accessibility
2. Allow Terminal or Python to control your computer
3. Check "Do Not Disturb" is disabled

### If program doesn't start / 如果程序不启动:
1. Ensure Python 3 is installed: `python3 --version`
2. Check file permissions: `ls -la mac_eyecare_fullscreen.py`
3. Try running with `--help` first

## 🆔 File Location / 文件位置

Settings are saved in: `~/.eyecare_fullscreen_settings.json`

Temporary HTML files are created in system temp directory and auto-cleaned.

## 🎉 Why This App is Different / 为什么此应用与众不同

**Most eye care apps are easy to ignore. This one ISN'T.**

**大多数护眼应用很容易忽略。这个不行。**

- ❌ Small notifications you can dismiss
- ❌ Gentle reminders you can postpone  
- ❌ Background apps you forget about

- ✅ **FULLSCREEN interruption**
- ✅ **Mandatory break time**
- ✅ **Beautiful, engaging experience**
- ✅ **Impossible to ignore**

## 🏆 Best Practices / 最佳实践

1. **Start with default settings** - They're scientifically based
2. **Use Mode 2** for the best experience
3. **Don't customize too much initially** - Build the habit first
4. **Take breaks seriously** - Your future self will thank you
5. **Use both languages** - Great for bilingual environments

---

**Protect your eyes, FORCE yourself to rest! 保护眼睛，强制休息！** 👁️‍🗨️✨

**Your vision is irreplaceable. Make this app work FOR you, not against you.**

**你的视力是不可替代的。让这个应用为你服务，而不是对抗你。**