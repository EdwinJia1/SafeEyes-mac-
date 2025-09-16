# macOS Eye Care Reminder / macOS护眼提醒

A bilingual eye protection reminder application designed specifically for macOS.

专为macOS设计的双语护眼提醒应用程序。

## Features / 功能特点

- **Bilingual Support / 双语支持**: English and Chinese (默认英语，可切换中文)
- **Native macOS Integration / 原生macOS集成**: Uses system notifications and dialogs
- **Customizable Timers / 可自定义计时器**: Configure work time, break time, and long break intervals
- **Smart Break System / 智能休息系统**: Short breaks and periodic long breaks
- **Persistent Settings / 持久化设置**: Your preferences are automatically saved
- **Command-line Interface / 命令行界面**: Easy to use terminal interface

## Installation / 安装

1. **Download the files / 下载文件**:
   - `mac_eyecare_native.py` - Main application
   - `start_eyecare.sh` - Startup script

2. **Make the startup script executable / 使启动脚本可执行**:
   ```bash
   chmod +x start_eyecare.sh
   ```

## Usage / 使用方法

### Interactive Mode / 交互模式
```bash
python3 mac_eyecare_native.py
# or / 或者
./start_eyecare.sh
```

### Direct Start / 直接启动
```bash
python3 mac_eyecare_native.py --start
# or / 或者
./start_eyecare.sh --start
```

### Configure Settings / 配置设置
```bash
python3 mac_eyecare_native.py --config
# or / 或者
./start_eyecare.sh --config
```

## Default Settings / 默认设置

- **Work Time / 工作时间**: 20 minutes / 20分钟
- **Break Time / 休息时间**: 20 seconds / 20秒
- **Long Break Time / 长休息时间**: 5 minutes / 5分钟
- **Cycles Before Long Break / 长休息前的周期**: 3 cycles / 3个周期
- **Language / 语言**: English / 英语
- **Notifications / 通知**: Enabled / 启用

## How It Works / 工作原理

1. **Work Period / 工作时段**: The app runs silently while you work
2. **Break Reminder / 休息提醒**: Shows macOS notification and dialog when it's time for a break
3. **Break Types / 休息类型**:
   - **Short Break / 短休息**: Brief eye rest (default 20 seconds)
   - **Long Break / 长休息**: Extended break for stretching (default 5 minutes every 3 cycles)

## Menu Options / 菜单选项

When running in interactive mode:

1. **Start reminder / 开始提醒**: Begin the eye care timer
2. **Stop reminder / 停止提醒**: Stop the running timer
3. **Show settings / 显示设置**: View current configuration
4. **Configure settings / 配置设置**: Modify timer intervals and language
5. **Switch language / 切换语言**: Toggle between English and Chinese
6. **Quit / 退出**: Close the application

## Customization / 自定义

You can customize:
- Work time (in minutes) / 工作时间（分钟）
- Break time (in seconds) / 休息时间（秒）
- Long break time (in minutes) / 长休息时间（分钟）
- Number of cycles before long break / 长休息前的周期数
- Language preference / 语言偏好

Settings are automatically saved in `~/.eyecare_settings.json`

## System Requirements / 系统要求

- macOS (any recent version)
- Python 3.6 or later
- Terminal access

## Tips for Eye Health / 护眼小贴士

### English:
- **20-20-20 Rule**: Every 20 minutes, look at something 20 feet away for 20 seconds
- **Blink More**: Computer users blink less frequently
- **Adjust Screen Position**: Top of screen should be at eye level
- **Use Proper Lighting**: Avoid glare and ensure adequate ambient lighting
- **Stay Hydrated**: Drink water regularly

### 中文:
- **20-20-20法则**: 每20分钟看20英尺外的物体20秒
- **多眨眼**: 使用电脑时眨眼频率会降低
- **调整屏幕位置**: 屏幕顶部应与眼睛平行
- **使用适当的照明**: 避免眩光并确保充足的环境照明
- **保持水分**: 定期喝水

## Troubleshooting / 故障排除

### If notifications don't appear / 如果通知不出现:
1. Check System Preferences → Notifications → Terminal → Allow notifications
2. Make sure "Do Not Disturb" is disabled
3. Try running with `--start` to test notifications

### If the program doesn't run / 如果程序无法运行:
1. Ensure Python 3 is installed: `python3 --version`
2. Check file permissions: `ls -la mac_eyecare_native.py`
3. Try running directly: `python3 mac_eyecare_native.py --help`

## License / 许可证

This software is provided as-is for personal use. Feel free to modify and distribute.

该软件按原样提供供个人使用。欢迎修改和分发。

---

**Protect your eyes, protect your future! / 保护眼睛，保护未来！** 👀✨