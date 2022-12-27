import pyautogui
import cv2
import keyboard
import time
import mouse
from pathlib import Path

KILL_SWITCH = "end"
event_active = True
event = 'winter'
web_center = (680, 584)
item_dist = 260 # num pixels between items
dim = pyautogui.size()
data_path = Path.joinpath(Path.cwd(), "survivor")

"""
- Image class will contain the path to the image (str), that images confidence level (mutable float),
if the image was being repeatedly clicked (bool), and the tbd location of the image
- Member functions to adjust confidence levels and repeated bool accordingly
"""
class Image:
    def __init__(self, img_path, img_confidence, img_repeated=False, img_loc=[0,0], img_region=(220,180,880,800)):
        self.path = img_path
        self.conf = img_confidence
        self.is_repeated = img_repeated
        self.loc = img_loc
        self.region = img_region
    
    def lower_confidence(self, scalar):
        self.conf -= scalar * 0.01

    def increase_confidence(self):
        self.conf += 0.01
        self.is_repeated = True

    def reset_confidence(self, img_confidence):
        self.conf = img_confidence
        self.is_repeated = False
        

# grab images from directory
images = [Image(str(file), 0.95) for file in data_path.iterdir() if file.suffix  == ".png" and file.is_file()]
if event_active:
    event_fp = Path(data_path, 'event_items', event)
    print(f"event items added from: {event_fp}")
    event_images = [Image(str(file), 0.95) for file in event_fp.iterdir() if file.suffix  == ".png" and file.is_file()]
    images = images + event_images

# sort items by priority
def get_last(image):
    return image.path[-5]
images.sort(key = get_last, reverse=True)

# look for high priority items locked on edge of web
priority_path = Path(data_path, 'locked_priority')
priority_images = [Image(str(file), 0.92) for file in priority_path.iterdir() if file.suffix == ".png" and file.is_file()]
priority_images.sort(key = get_last, reverse=True)

# prestige image to search for if no items found
prestige_path1 = Path(data_path, "../informational/prestige-1.png")
prestige_path2 = Path(data_path, "../informational/prestige-2.png")
prestige_img1 = Image(str(prestige_path1), 0.9, img_region=(570,470,210,210))
prestige_img2 = Image(str(prestige_path1), 0.9, img_region=(570,470,210,210))


def find_priority_item():
    for img in priority_images:
        loc = pyautogui.locateCenterOnScreen(img.path, confidence=img.conf, grayscale=True,
                                        region=img.region)

        if loc:
            print("found priority item")
            return loc

    if not loc:
        print("no priority item exists")
        return None


if __name__ == "__main__":    
    list_iterations = 0 # keeps track of how many iterations of search without finding img
    repeat_attempts = 0 # keeps track of how many times a grayed image clicked on
    flag = False # used to break out of nested loop
    last_img = images[-1] # used to check if all images iterated through

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

        # find bloodpoint count to compare later to determine successful bloodweb purchase
        bp_screencap = pyautogui.screenshot("generated/bp.png", region=(1465,60, 110,30))
        bp_img = Image("generated/bp.png", 0.95, img_region=(1465,60, 110,30))
        time.sleep(1)

        for img in images:
            print(f"{img.path} | {img.conf} | {repeat_attempts}")

            # locate the img of item in folder
            # converting to grayscale imporves performance, confidence adjusts how accurate the match it,
            # and region (left, top, width, height) bounds the dimensions of search window
            img.loc = pyautogui.locateCenterOnScreen(img.path, confidence=img.conf,
                                            grayscale=True, region=img.region)

            if img.loc: # if img found, returns coordinates of center
                list_iterations = 0 # reset attempts to 0 img found

                print(f"Found: {img.path} @{img.loc}")
                mouse.move(img.loc[0], img.loc[1]) # move mouse to img location
                time.sleep(0.25)
                pyautogui.mouseDown() # click image and hold it down before releasing
                time.sleep(1.2)
                pyautogui.mouseUp()
                mouse.move(int(0.75*dim[0]), int(0.45*dim[1])) # move to side of screen to not effect other images
                print(img.loc)
                
                # check if valid transaction
                bp_img_loc = pyautogui.locateCenterOnScreen(bp_img.path, confidence=bp_img.conf,
                            grayscale=False, region=bp_img.region)

                if bp_img_loc: # if img found, indicates user's bloodpoints are unchanged
                    img.increase_confidence()
                    repeat_attempts += 1
                    print(f"Repeat image detected, increasing confidence to {img.conf}")   
                else:
                    repeat_attempts = 0
                    print("Transaction successful")           
                
                if repeat_attempts == 3: # if 3 attempts in a row click an invalid image, increase all confidence
                    for img in images:
                        img.increase_confidence()
                        repeat_attempts = 0
                    print("Confidence increase")

                if img.conf <= 0.92: # threshold confidence value that means all images are too low
                    for img in images:
                        img.reset_confidence(0.95)

                break # return to top of list to ensure highest priority found first

            if list_iterations > 3:
                flag = True
                print("attempts exceeded")
                break
            if keyboard.is_pressed(KILL_SWITCH):
                flag = True
                print("kill switch pressed")
                break

        prestige_img1.loc = pyautogui.locateCenterOnScreen(prestige_img1.path, confidence=prestige_img1.conf,
                        grayscale=False,region=prestige_img1.region)
        prestige_img2.loc = pyautogui.locateCenterOnScreen(prestige_img2.path, confidence=prestige_img2.conf,
                        grayscale=False,region=prestige_img2.region)

        if prestige_img1.loc or prestige_img2.loc: # check for prestige icon
            if prestige_img1.loc:
                mouse.move(prestige_img1.loc[0], prestige_img1.loc[1])
            if prestige_img2.loc:
                mouse.move(prestige_img2.loc[0], prestige_img2.loc[1])
            print("Prestiging...")
            time.sleep(0.25)
            pyautogui.mouseDown()
            time.sleep(5)
            pyautogui.mouseUp()
            mouse.move(int(0.75*dim[0]), int(0.45*dim[1]))
            time.sleep(1)

        if flag == True:
            break

        list_iterations +=  1

        if list_iterations > 0 and img.path == images[-1].path: # if iterated through all images and found nothing, lower img conf
            for img in images:
                img.lower_confidence(1)
        