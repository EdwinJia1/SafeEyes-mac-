#!/bin/bash

# Eye Care Reminder with Fullscreen Support
# 全屏护眼提醒启动脚本

echo "🔥 FULLSCREEN Eye Care Reminder for macOS 🔥"
echo "全屏护眼提醒程序"
echo "=========================================="
echo ""
echo "This version includes POWERFUL fullscreen reminders:"
echo "此版本包含强力全屏提醒："
echo "• Mode 1: Large Dialog (大对话框)"
echo "• Mode 2: Fullscreen HTML Page (全屏HTML页面)"
echo "• Mode 3: System Modal Dialog (系统模态对话框)"
echo ""

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "错误：未安装Python 3或不在PATH中"
    exit 1
fi

echo "Starting fullscreen eye care reminder..."
echo "启动全屏护眼提醒..."
echo ""

python3 "$DIR/mac_eyecare_fullscreen.py" "$@"