import win32api
import win32gui
from win32.lib import win32con
import time
import sys


def auto_input(window_title, text):
    win_title = window_title
    while True:
        hwnd = win32gui.FindWindow(None, win_title)
        if not hwnd:
            time.sleep(1)
            continue
        win32gui.SetForegroundWindow(hwnd)
        for i in text:
            if i.isupper():
                win32api.keybd_event(win32con.VK_SHIFT, win32api.MapVirtualKey(win32con.VK_SHIFT, 0), 0, 0)
                time.sleep(0.05)
            win32api.keybd_event(ord(i.upper()), win32api.MapVirtualKey(ord(i.upper()), 0), 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(ord(i.upper()), win32api.MapVirtualKey(ord(i.upper()), 0), win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.05)
            if i.isupper():
                win32api.keybd_event(win32con.VK_SHIFT, win32api.MapVirtualKey(win32con.VK_SHIFT, 0),
                                     win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(0.05)
        return


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("参数错误\n python auto_input.py WindowTitle Text\n")

    auto_input(sys.argv[1], sys.argv[2])
