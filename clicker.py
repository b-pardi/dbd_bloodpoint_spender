import pyautogui
import keyboard
import time
import mouse
from pathlib import Path

KILL_SWITCH = "end"
event_active = True
event = 'winter'
web_center = (680, 584)
item_dist = 260

dim = pyautogui.size()
data_path = Path.joinpath(Path.cwd(), "survivor")

# grab images from directory
images = [str(file) for file in data_path.iterdir() if file.suffix  == ".png" and file.is_file()]
if event_active:
    event_fp = Path(data_path, 'event_items', event)
    print(f"event items added from: {event_fp}")
    event_images = [str(file) for file in event_fp.iterdir() if file.suffix  == ".png" and file.is_file()]
    images = images + event_images

# sort items by priority
def get_last(str):
    return str[-5]
images.sort(key = get_last, reverse=True)

# look for high priority items locked on edge of web
priority_path = Path(data_path, 'locked_priority')
priority_images = [str(file) for file in priority_path.iterdir() if file.suffix == ".png" and file.is_file()]
priority_images.sort(key = get_last, reverse=True)

def find_priority_item():
    for img in priority_images:
        loc = pyautogui.locateCenterOnScreen(img, confidence = 0.93, grayscale=True,
                                        region=(220,200,880,780))
        if loc:
            print("found priority item")
            return loc
    if not loc:
        print("no priority item exists")
        return None


if __name__ == "__main__":    
    attempts = 0 # keeps track of how many iterations of search without finding img
    flag = False # used to break out of nested loop
    while True:
        priority_img = find_priority_item()
        if priority_img: # if there is a priorty item on the fringe of web
            print(priority_img)
            
            '''
            search for imgs within 'item_dist' away from priority img
                optimally, use loc of item rel to center to look in certain direction only
                    i.e. if item is in 3rd quadrant (bottom left), look only above, right, or diag upper right
                    since it won't be any more to the bottom left
            if no imgs found adjacent, check grayed out imgs as well, and save their locations
                gray locations can be found by searching normal images with a lowered confidence (~0.75)
                if grayed imgs found adjacent, check around them as well until a selectable (not grayed out) perk shows
            once selectable perk found, iterate back up list towards the priority item
            '''

        for img in images:
            print(img)
            # locate the img of item in folder
            # converting to grayscale imporves performance, confidence adjusts how accurate the match it,
            # and region (left, top, width, height) bounds the dimensions of search window
            loc = pyautogui.locateCenterOnScreen(img, confidence = 0.94, grayscale=True,
                                            region=(220,200,880,780))
            if loc: # if img found, returns coordinates of center
                attempts = 0 # reset attempts to 0 when img found
                print(f"Found: {img} @{loc}")
                mouse.move(loc[0], loc[1])
                time.sleep(0.25)
                pyautogui.mouseDown()
                time.sleep(1.2)
                pyautogui.mouseUp()
                mouse.move(int(0.75*dim[0]), int(0.45*dim[1]))
                time.sleep(1)
                print(loc)
                break # return to top of list to ensure highest priority found first

            if attempts > 3:
                flag = True
                print("attempts exceeded")
                break
            if keyboard.is_pressed(KILL_SWITCH):
                flag = True
                print("kill switch pressed")
                break

        if flag == True:
            break
        attempts +=  1
        