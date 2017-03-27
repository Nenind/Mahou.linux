import keyboard
import pyperclip
import threading
import time
import datetime
from by_dict_conversion import buildDict, convert

cword = []
_self = False
cThread = threading.Thread()
hotkeys = ["f7", "f6", "f4"]
clearkeys = ["space", "enter", "home", "end", "esc", "tab", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "win", "left", "up", "right", "down"]
dict = buildDict()

def gettime(time: float):
    return datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S.%f')

def KeyboardHookCallback(kbd_event: keyboard.KeyboardEvent):
    """Main keyboard hook callback."""
    global cword
    global _self
    scan = kbd_event.scan_code
    name = kbd_event.name
    event = kbd_event.event_type
    if not _self and name not in hotkeys:
        if event == 'down':
            if name == 'backspace':
                cword.pop()
            elif name in clearkeys:
                cword = []
            else:
                cword.append(scan)
        print("Key with name: [" + name + "] and scan: [" + str(scan) + "] -> [" + event + "] in "+gettime(kbd_event.time)+".")

def endedConversion(sleep_time, hotkey, action):
    global _self
    global cThread
    time.sleep(sleep_time)
    _self = False
    keyboard.register_hotkey(hotkey, action)
    print("Ended Conversion. (" + str(sleep_time) +")")

def ConvertLast():
    global _self
    global cThread
    print("OK "+str(len(cword)))
    if not _self:
        _self = True
        keyboard.remove_hotkey('f7')
        sleep_time = len(cword) * 2 * 0.02 # Calculate time to sleep, 10 ms for every character
        for i in range(0, len(cword)):
            keyboard.press_and_release('backspace')
        keyboard.press_and_release('alt+shift')
        for scan in cword:
            keyboard.press_and_release(scan)
        if not cThread.is_alive(): # Prevent already started thread exception
            cThread = threading.Thread(target=endedConversion, args=(sleep_time,'f7',ConvertLast,))
            cThread.start()
def ConvertSelection():
    global _self
    global cThread
    bkp = pyperclip.paste()
    pyperclip.copy('')
    keyboard.press_and_release('ctrl+c')
    ClipStr = pyperclip.paste()
    if ClipStr != "":
        _self = True
        keyboard.press_and_release('backspace')
        sleep_time = len(ClipStr) * 0.02 # Calculate time to sleep, 10 ms for every character
        keyboard.write(convert(ClipStr, dict))
        if not cThread.is_alive():
            cThread = threading.Thread(target=endedConversion, args=(sleep_time,'f6',ConvertSelection,))
            cThread.start()
    pyperclip.copy(bkp)
keyboard.register_hotkey('f7', ConvertLast)
keyboard.register_hotkey('f6', ConvertSelection)
keyboard.hook(KeyboardHookCallback)
keyboard.wait('f4')