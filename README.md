# Dead By Daylight BloodPoint Spender
## Automated bot to spend blood points in the blood web of the game Dead By Daylight. **DOES NOT EFFECT GAMEPLAY.**


![Title Card](https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/3/3d/Header_5thAnniversary.jpg/revision/latest?cb=20210602112536)


### ***NOTE:*** as it stands, the methods used in this program will not scale well. Monitor sizes other than 1080p will not work properly, and some items are not recognized consistently causing it to get stuck. A new method via image classification with machine learning is being investigated and will hopefully have updates shortly.


## To use the program as it is:
+ Launch the game on a 1080p monitor (or scale down to 1080p) and navigate to the bloodweb of whatever character you would like to spend bp on
+ open a terminal or code editor either on a 2nd monitor or ontop of the game
+ run the script 'clicker.py'
+ make sure nothing is blocking the view of the items in the blood web. If you can't see it, neither can the program!
+ check occasionally to make sure it doesn't get stuck


## FAQ
> Will this work with killers too?

No, once the survivor functionality is working properly, I will implement a killer blood point spender as well. But it doesn't make much sense to invest all that time into a killer one currently while the survivor one is flawed

> why does it not recognize some of the perks?

Honestly good question for the pyautogui developers. It is one of the main reasons I'm trying a new method from scratch.

> Why does it only work on 1080p monitors?

The program looks for screenshots of images of perks and they have to match the correct size. the screenshots were all taken on 1080p monitor so the size of the screenshots will differ from the size of the perks on different resolution monitors. This is the other main reason I'm trying a new method
