import keyboard
from keyboard import mouse
import pyperclip
import threading
import time
import os
import sys
import datetime
from by_dict_conversion import buildDict, convert


sim = True
logging = False
__version__ = '0.254'
flag = False
cword = []
_self = False
cThread = threading.Thread()
hotkeys = ["shift", "ctrl+shift+X", "f4", "capslock"]
clearkeys = ['backspace', 'left windows', 'enter', 'home', 'end', "esc", "tab", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "win", "windows", "left", "up", "right", "down"]
dict = buildDict()

def gettime(time: float):
    return datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S.%f')

def KeyboardHookCallback(kbd_event: keyboard.KeyboardEvent):
    """Main keyboard hook callback."""
    global cword
    global _self
    global logging
    scan = kbd_event.scan_code
    name = kbd_event.name
    event = kbd_event.event_type
    if not _self and name not in hotkeys:
        if event == 'down':
            # if name == 'backspace':
            #     cword.pop()
            if name in clearkeys:
                cword.clear()
            else:
                cword.append(scan)
        if logging:
            print("Key with name: [" + name + "] and scan: [" + str(scan) + "] -> [" + event + "] in "+gettime(kbd_event.time)+".")

def MouseHookCallBack(m_event: mouse.ButtonEvent):
    """Main mouse hook callback."""
    global cword
    global logging
    if hasattr(m_event, 'event_type'):
        if logging:
            print("Mouse event -> " + m_event.event_type)
        cword.clear()

def endedConversion(sleep_time, hotkey, action):
    global _self
    global cThread
    global logging
    time.sleep(sleep_time)
    _self = False
    keyboard.register_hotkey(hotkey, action)
    if logging:
        print("Ended Conversion. (" + str(sleep_time) +")")
def ChangeLayout():
    global sim
    if sim:    
        # Changing layout by Alt+Shift
        keyboard.press_and_release("alt+shift")
    else:
        # Changing layout using system
        os.system('bash ./change-layout.sh')



def ConvertLast():
    global cword
    global _self
    global cThread
    global flag
    global curtime
    if flag:
        if round(time.time()*1000)-curtime < 500:
            print("OK "+str(len(cword)))
            if not _self and len(cword) > 0:
                _self = True
                sleep_time = 0
                # sleep_time = len(cword) * 2 * 0.005                 # Calculate time to sleep, 5 ms for every character
                for i in range(0, len(cword)):
                    keyboard.press_and_release('backspace')
                ChangeLayout()
                for scan in cword:
                    keyboard.press_and_release(scan)
                if not cThread.is_alive():
                    cThread = threading.Thread(target=endedConversion, args=(sleep_time,'f7',ConvertLast,))
                    cThread.start()
                time.sleep(0.05)
        flag = False
    else:
        flag = True
        curtime = round(time.time()*1000)
    
    
def ConvertSelection():
    global _self
    global cThread
    bkp = pyperclip.paste()
    pyperclip.copy('')
    keyboard.press_and_release('ctrl+c')
    ClipStr = pyperclip.paste()
    print(ClipStr)
    if ClipStr != "":
        _self = True
        keyboard.press_and_release('backspace')
        sleep_time = len(ClipStr) * 0.005
        pyperclip.copy(convert(ClipStr, dict))
        print(pyperclip.paste())
        keyboard.write(convert(ClipStr, dict))
        time.sleep(0.05)
        if not cThread.is_alive():
            cThread = threading.Thread(target=endedConversion, args=(sleep_time,'f6',ConvertSelection,))
            cThread.start()
    pyperclip.copy(bkp)
def Init():
    global logging
    if len(sys.argv) > 1:
        if sys.argv[1] == '-l':
            logging = True
    keyboard.register_hotkey(hotkeys[0], ConvertLast)
    keyboard.register_hotkey(hotkeys[1], ConvertSelection)
    keyboard.hook(KeyboardHookCallback)
    mouse.hook(MouseHookCallBack)
    print("""Hotkeys:
    Double SHIFT to convert last line.
    CTRL+SHIFT+X to convert selection.
    F4 to close Mahou.linux.""")
    keyboard.wait(hotkeys[2])

if __name__ == '__main__':
    Init()