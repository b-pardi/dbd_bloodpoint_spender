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

DIR = dir1

while 1:
    if keyboard.is_pressed(CAP_KEY):
        num_dups = 0
        mouse_pos = pyautogui.position()
        region = (mouse_pos[0], mouse_pos[1], 58, 60)
        im = pyautogui.screenshot("temp.png", region=region)
        fn = input("What is the name of this item? ")
        priority = input("What is item priority? ")
        try:
            os.rename("temp.png", DIR + fn + '-' + priority + '.png')
            print(f"renamed to: {DIR + fn + '-' + priority}.png")
        except:
            if input("file already exists, add duplicate? (y or n): ") == 'y':
                num_dups = len([name for name in os.listdir(DIR)
                    if os.path.isfile(os.path.join(DIR, name))
                    and name.__contains__(fn)])
                print(f"appending {num_dups}")
                os.rename("temp.png", DIR + fn + '-' + str(num_dups+1) + '-' + priority + '.png')
                print(f"renamed to: {DIR + fn + '-' + str(num_dups+1) + '-' + priority}.png")
    
    if keyboard.is_pressed(CANCEL_KEY):
        os.remove(DIR + fn+ '-' + priority+'.png')
        print("Removed previous image")
        time.sleep(0.5)

    if keyboard.is_pressed(KILL_SWITCH):
        break
