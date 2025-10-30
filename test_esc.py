#!/usr/bin/env python3
"""
Test script for ESC key detection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mac_eyecare_fullscreen import KeyboardListener
import time

def test_esc_detection():
    print("🎯 Testing ESC key detection...")
    print("Press ESC key to test, or Ctrl+C to exit.")
    print("This test will run for 10 seconds.")

    try:
        with KeyboardListener() as kb:
            for i in range(10, 0, -1):
                print(f"\rTesting... {i} seconds remaining", end="", flush=True)

                # Check for ESC key
                if kb.check_for_esc(0.1):
                    print("\n✅ ESC key detected successfully!")
                    return True

                time.sleep(1)

            print("\n⏰ Time's up - ESC key not pressed")
            return False

    except Exception as e:
        print(f"\n❌ Error testing ESC key: {e}")
        return False

if __name__ == "__main__":
    test_esc_detection()