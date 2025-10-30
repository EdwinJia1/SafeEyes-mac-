#!/usr/bin/env python3
"""
Test script to verify terminal reset functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mac_eyecare_fullscreen import KeyboardListener, reset_terminal
import time

def test_terminal_reset():
    print("🧪 Testing terminal reset functionality...")
    print("This will test keyboard listener and terminal restoration.")
    print("Test will run for 5 seconds. You can press ESC to test early.\n")

    try:
        print("Before keyboard listener - terminal should be normal.")
        time.sleep(1)

        # Test keyboard listener
        with KeyboardListener() as kb:
            print("Inside keyboard listener context...")
            for i in range(5, 0, -1):
                print(f"\rTesting... {i} seconds remaining (Press ESC to test)", end='', flush=True)

                if kb.check_for_esc(0.1):
                    print("\n✅ ESC key detected! Testing terminal reset...")
                    break
                time.sleep(1)

        # Keyboard listener should have exited and restored terminal
        print("\n\nExited keyboard listener context.")
        reset_terminal()

        print("✅ Terminal reset test completed!")
        print("If you can read this clearly, the terminal was restored properly.")
        print("If text appears garbled or with strange characters, there may be an issue.")

        return True

    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        return False

if __name__ == "__main__":
    success = test_terminal_reset()
    if success:
        print("\n🎯 Test passed! Terminal handling appears to be working correctly.")
    else:
        print("\n⚠️ Test failed. There may be terminal handling issues.")