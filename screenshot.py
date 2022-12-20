import pyautogui
import keyboard
import os
import time

CAP_KEY = "home"
CANCEL_KEY = "esc"
KILL_SWITCH = "end"
dir1 = 'survivor/'
dir2 = 'survivor/locked/'
dir3 = 'survivor/locked_priority/'

dir = dir1

while 1:
    if keyboard.is_pressed(CAP_KEY):
        mouse_pos = pyautogui.position()
        region = (mouse_pos[0], mouse_pos[1], 54, 54)
        im = pyautogui.screenshot("temp.png", region=region)
        fn = input("What is the name of this item? ")
        priority = input("What is item priority? ")
        os.rename("temp.png", dir + fn + '-' + priority + '.png')
        print(f"renamed to: {dir + fn+ '-' + priority}.png")
    
    if keyboard.is_pressed(CANCEL_KEY):
        os.remove(dir + fn+ '-' + priority+'.png')
        print("Removed previous image")
        time.sleep(0.5)

    if keyboard.is_pressed(KILL_SWITCH):
        break
