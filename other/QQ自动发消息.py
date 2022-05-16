import win32gui
import win32con
import win32api
import win32clipboard
import time
from pynput import keyboard
from pynput.keyboard import Key, Controller
from pynput.keyboard import Listener

k = Controller()


def getText():
    """获取剪贴板文本"""
    win32clipboard.OpenClipboard()
    d = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return d


def setText(aString):
    """设置剪贴板文本"""
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    win32clipboard.CloseClipboard()


def on_activate():
    
    print('Global hotkey activated!')

    handle = win32gui.FindWindow(None, '杨洋')

    win32gui.SetForegroundWindow(handle)
    # 激活当前窗口

    win32gui.SendMessage(handle, win32con.WM_PASTE, 0, 0)
    # 粘贴剪切板的消息
    # 部分程序屏蔽该api

    k.type("Hello World !")
    k.press(Key.enter)
    k.release(Key.enter)


def for_canonical(f):
    print(f)
    return lambda k: f(l.canonical(k))


hotkey = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+<alt>+h'), on_activate)

with keyboard.Listener(on_press=for_canonical(hotkey.press),
                       on_release=for_canonical(hotkey.release)) as l:
    l.join()
