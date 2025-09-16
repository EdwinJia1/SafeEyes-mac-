#!/usr/bin/env python3
"""
Debug script to test HTML generation and Safari opening
"""

import tempfile
import subprocess
import webbrowser
import os

def create_test_html():
    """Create a simple test HTML file"""
    
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Eye Care Reminder</title>
    <style>
        body {
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
        }
        
        /* Sky background with fluffy clouds */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 70%;
            background: 
                radial-gradient(ellipse 300px 100px at 20% 30%, rgba(255,255,255,0.9) 40%, transparent 60%),
                radial-gradient(ellipse 400px 120px at 70% 25%, rgba(255,255,255,0.7) 40%, transparent 60%),
                radial-gradient(ellipse 250px 80px at 85% 40%, rgba(255,255,255,0.8) 40%, transparent 60%);
            z-index: -2;
            animation: cloud-drift 20s ease-in-out infinite;
        }
        
        /* Grass at bottom */
        body::after {
            content: '';
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 35%;
            background: linear-gradient(180deg, #90EE90 0%, #32CD32 40%, #228B22 100%);
            z-index: -1;
        }
        
        .reminder-container {
            text-align: center;
            max-width: 800px;
            padding: 60px 40px;
            background: rgba(255, 255, 255, 0.92);
            border-radius: 25px;
            backdrop-filter: blur(15px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.6);
            color: #2F4F4F;
            position: relative;
            z-index: 10;
        }
        
        .title {
            font-size: 4rem;
            font-weight: 700;
            margin-bottom: 30px;
            color: #2E8B57;
            text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.8);
            animation: gentle-pulse 3s infinite;
        }
        
        .sun {
            position: fixed;
            top: 10%;
            right: 15%;
            font-size: 4rem;
            color: #FFD700;
            animation: sun-glow 6s infinite;
            z-index: -1;
        }
        
        .birds {
            position: fixed;
            top: 25%;
            left: 20%;
            font-size: 1.5rem;
            color: #696969;
            animation: fly 20s infinite linear;
            z-index: -1;
        }
        
        .flowers {
            position: fixed;
            bottom: 10%;
            left: 10%;
            font-size: 2rem;
            z-index: -1;
            animation: sway 4s ease-in-out infinite;
        }
        
        @keyframes gentle-pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        
        @keyframes sun-glow {
            0%, 100% { opacity: 0.8; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.1); }
        }
        
        @keyframes fly {
            0% { transform: translateX(-100px); }
            100% { transform: translateX(calc(100vw + 100px)); }
        }
        
        @keyframes sway {
            0%, 100% { transform: rotate(-2deg); }
            50% { transform: rotate(2deg); }
        }
        
        @keyframes cloud-drift {
            0%, 100% { transform: translateX(0px); }
            50% { transform: translateX(30px); }
        }
        
        .message {
            font-size: 2rem;
            color: #4682B4;
            margin-bottom: 30px;
        }
        
        .close-btn {
            font-size: 1.5rem;
            background: #32CD32;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            margin-top: 30px;
        }
        
        .close-btn:hover {
            background: #228B22;
        }
    </style>
</head>
<body>
    <!-- Natural decoration elements -->
    <div class="sun">☀️</div>
    <div class="birds">🕊️ 🕊️</div>
    <div class="flowers">🌸 🌼 🌻</div>
    
    <div class="reminder-container">
        <div style="font-size: 5rem; margin-bottom: 20px;">👁️</div>
        <h1 class="title">TEST: 护眼提醒测试</h1>
        <div class="message">如果你能看到这个美丽的蓝天白云页面，说明程序正常工作！</div>
        <div class="message">If you can see this beautiful sky page, the program is working!</div>
        <button class="close-btn" onclick="window.close()">关闭 / Close</button>
    </div>

    <script>
        // Auto-focus for immediate key response
        window.focus();
        
        // Close on keypress
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' || event.key === 'Escape' || event.key === ' ') {
                window.close();
            }
        });
    </script>
</body>
</html>
    """
    
    return html_content

def test_html_creation():
    """Test HTML file creation and opening"""
    
    print("🧪 Testing HTML file creation and Safari opening...")
    
    try:
        # Create HTML content
        html_content = create_test_html()
        print("✅ HTML content created successfully")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_content)
            html_file = f.name
        
        print(f"✅ Temporary HTML file created: {html_file}")
        
        # Check if file exists and readable
        if os.path.exists(html_file):
            print(f"✅ File exists and is readable")
            with open(html_file, 'r') as f:
                content = f.read()
            print(f"✅ File size: {len(content)} characters")
        else:
            print("❌ File does not exist!")
            return
        
        # Try opening with Safari
        print("🌐 Attempting to open with Safari...")
        result = subprocess.run([
            'open', '-a', 'Safari', html_file
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Safari command executed successfully")
        else:
            print(f"❌ Safari command failed: {result.stderr}")
        
        # Also try with default browser
        print("🌐 Also trying with default browser...")
        webbrowser.open(f'file://{html_file}')
        
        print(f"\n📁 HTML file location: {html_file}")
        print("📝 You can also open this file manually to test")
        
        return html_file
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return None

if __name__ == '__main__':
    test_file = test_html_creation()
    
    input("\nPress Enter to delete the test file and exit...")
    
    # Clean up
    if test_file and os.path.exists(test_file):
        os.unlink(test_file)
        print("🗑️ Test file deleted")