#!/bin/bash

# Eye Care Reminder Startup Script for macOS
# 护眼提醒启动脚本

echo "Eye Care Reminder for macOS"
echo "护眼提醒程序"
echo "=========================="

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "错误：未安装Python 3或不在PATH中"
    exit 1
fi

# Start the eye care reminder
echo "Starting eye care reminder..."
echo "启动护眼提醒..."
echo ""

python3 "$DIR/mac_eyecare_native.py" "$@"