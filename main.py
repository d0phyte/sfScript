from pyautogui import *
import pyautogui
import time
import keyboard
import numpy as np
import random
import win32api, win32con
import pytesseract
from PIL import Image
import cv2

# Specify the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
time.sleep(3)

#for special events like hellevator, all menu positions change and click functions need to be updated. Need to use shortcuts in every click to prevent this or update manually
#event = 0

allTavernChars = [
    "TavernCharacters/TavernChar1.png", "TavernCharacters/TavernChar2.png","TavernCharacters/TavernChar3.png","TavernCharacters/TavernChar4.png",
    "TavernCharacters/TavernChar5.png","TavernCharacters/TavernChar6.png","TavernCharacters/TavernChar7.png","TavernCharacters/TavernChar8.png",
    "TavernCharacters/TavernChar9.png","TavernCharacters/TavernChar10.png"]
#xp numbers region
regionIsTheSame = (1093, 645, 150, 50)

#testing = pyautogui.screenshot(region=regionIsTheSame)
#testing.save("testingRegions.png")

#quest time region
timerRegion = (1308, 649, 110, 50)

#thirst for adventure region
thirstRegion = (1283, 945, 58, 48)

#checking mouse position in idle shell: 
#import pyautogui
#pyautogui.displayMousePosition()

#function for identifying which character is present in the tavern
def identifyTavChar(whatCharacter):
    time.sleep(0.1)
    for char in whatCharacter:
        try:
            location = pyautogui.locateCenterOnScreen(char, confidence=0.7)
            if location is not None:
                print(f"Found image {char} on screen at {location}.")
                # Unpack the location tuple (x, y) and call the custom click function
                x, y = location
                click(x, y) #click character after identity is confirmed
                time.sleep(2)
                return char
        except pyautogui.ImageNotFoundException:
           
            print("Looking for tavern character.")

    print("No images found on screen.")
    return None

#click(coordinates x and y on screen) Use this function to choose where to left mouse click. 
def click(x,y):
    x += random.randint(-5, 5)
    y += random.randint(-5, 5)
    pyautogui.moveTo(x, y, 1) #more human like movement
    #win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(np.random.uniform(0.3,0.7))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

#gets the xp number from the quest on screen
def pickQuest(regionIsTheSame):
    xp_screenshot = pyautogui.screenshot(region=regionIsTheSame)
    xp_screenshot.save("xp_debug.png") 
    #this function is also being used to get the time, in the end it will save a screenshot of the time, but we can see the xp numbers in between
    #could be done better by creating a new function for time, but ok for now
    time.sleep(np.random.uniform(0.3, 0.7))
    
    image = np.array(xp_screenshot)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789'  # Only numbers
    xpNumber = pytesseract.image_to_string(gray, config=custom_config)
    time.sleep(np.random.uniform(0.3, 0.7))
    
    print("Xp number:", xpNumber)
    
    # If the XP number is empty, return None or a default value (e.g., 0)
    if xpNumber.strip() == "":  # Check if xpNumber is empty
        print("No XP number detected. Assigning a default value of 0.")
        return 0  # You can also return None if you want to handle it differently
    else:
        try:
            return int(xpNumber.strip())  # Convert the number to an integer after stripping any extra spaces
        except ValueError:
            print(f"Error: Invalid XP number detected: {xpNumber}")
            return 0  # Default to 0 if conversion fails

def checkThirst():

    try:
        time.sleep(1)
        noEnergy = pyautogui.locateCenterOnScreen('noThirstLeft.png', confidence = 0.8)
        if noEnergy:
            print('No energy, time for a drink!')
            #click bartender
            click(1751,479)
            time.sleep(1)

            #click drink button, its better to do it with clicks. If we spam enter it might start another quest by mistake
            for _ in range(5):
                click(1167, 682)
                print("Drinking a beer")
                time.sleep(1)

            noEnergy = pyautogui.locateCenterOnScreen('noThirstLeft.png', confidence = 0.8)

            if noEnergy:
                print('No more drinks today, stopping script')
                menuGuard()
                exit()

            else:
                print('Feeling better now, time for a quest!')
                pyautogui.keyDown('f')
                time.sleep(np.random.uniform(0.3,0.7))        
                pyautogui.keyUp('f')
                pyautogui.keyDown('t')
                time.sleep(np.random.uniform(0.3,0.7))        
                pyautogui.keyUp('t')


    except pyautogui.ImageNotFoundException:
        print('Still have energy, time for a quest!')
        pyautogui.keyDown('m')
        time.sleep(np.random.uniform(0.3,0.7))        
        pyautogui.keyUp('m')
        pyautogui.keyDown('t')
        time.sleep(np.random.uniform(0.3,0.7))        
        pyautogui.keyUp('t')

        

def pressEnter():
    time.sleep(np.random.uniform(0.3,0.7))
    pyautogui.keyDown('enter')
    time.sleep(np.random.uniform(0.3,0.7))
    pyautogui.keyUp('enter')
    time.sleep(1)    

def menuTavern():
    pyautogui.keyDown('t')
    time.sleep(np.random.uniform(0.3,0.7))        
    pyautogui.keyUp('t')
    time.sleep(1)

def menuGuard(): #City Guard when no energy/thirst is left
    pyautogui.keyDown('f')
    time.sleep(np.random.uniform(0.3,0.7))        
    pyautogui.keyUp('f')
    time.sleep(np.random.uniform(0.3,0.7))
    pyautogui.keyDown('t')
    time.sleep(np.random.uniform(0.3,0.7))        
    pyautogui.keyUp('t')
    time.sleep(np.random.uniform(0.3,0.7))
    pyautogui.keyDown('t')
    time.sleep(np.random.uniform(0.3,0.7))        
    pyautogui.keyUp('t')
    time.sleep(np.random.uniform(0.3,0.7))

    for _ in range (9):
        time.sleep(np.random.uniform(0.1,0.2))
        pyautogui.keyDown('right')
        time.sleep(np.random.uniform(0.1,0.2))
        pyautogui.keyUp('right')

    time.sleep(np.random.uniform(0.3,0.7))
    pyautogui.keyDown('enter')
    time.sleep(np.random.uniform(0.3,0.7))
    pyautogui.keyUp('enter')


#tavern, main gameplay loop. Works most of the time, sometimes assumes wrong xp number and picks wrong quest.
def tavernLoop():

        numbers_region1 = pickQuest(regionIsTheSame)
        
        pyautogui.keyDown('right')
        time.sleep(np.random.uniform(0.3,0.7))        
        pyautogui.keyUp('right')
        

        numbers_region2 = pickQuest(regionIsTheSame)
        
        pyautogui.keyDown('right')
        time.sleep(np.random.uniform(0.3,0.7))        
        pyautogui.keyUp('right')
        #separate with arrow key presses to change quest screen

        numbers_region3 = pickQuest(regionIsTheSame)
        
        questxp1 = int(numbers_region1)
        questxp2 = int(numbers_region2)
        questxp3 = int(numbers_region3)
        
        #ALL DONE, NOW JUST PICK THE HIGHEST XP AND GO WITH THAT MISSION

        if questxp1 > questxp2 and questxp1 > questxp3:
            #move back to first quest and pick it
            print('Picked first quest')
            click(909,359) #these clicks scroll to the quest, this one to the first one, for example
            

        elif questxp2 > questxp1 and questxp2 > questxp3:
            #pick second quest
            print('Picked second quest')
            click(1176,362)

        elif questxp3 > questxp1 and questxp3 > questxp2:
            #pick third quest
            print('Picked third quest')
            click(1452,360)

            
        else:
            # Handle ties: collect quests tied with the same XP
            max_xp = max(questxp1, questxp2, questxp3)
            choices = []

            if questxp1 == max_xp:
                choices.append((909, 359, 'first quest'))
            if questxp2 == max_xp:
                choices.append((1176, 362, 'second quest'))
            if questxp3 == max_xp:
                choices.append((1452, 360, 'third quest'))

            # Randomly pick one of the tied quests
            x, y, quest_name = random.choice(choices)
            print(f'Picked {quest_name}')
            click(x, y)

        time.sleep(2)
        #before pressing the accept button, check timer area and register how long the quest travel time will be
        #make sure you have a mount so there is a small margin. Quest ends before program moves on.
        #Need to make a mount checker when the program is run first time

        questLenght = pickQuest(timerRegion)/100
        print(f'Quest started. ({questLenght} minutes in total)')
        timerDuration = questLenght * 60
        startTime = time.time()

        #this click actually presses the accept button
        click(1182,764)
        time.sleep(2)
        click(328,935)

        while True:
            elapsedTime = time.time() - startTime

            if elapsedTime > timerDuration:
                print('Quest finished, back to the tavern')
                
                pyautogui.keyDown('f')
                time.sleep(np.random.uniform(0.3,0.7))        
                pyautogui.keyUp('f')
                time.sleep(np.random.uniform(0.3,0.7))
                pyautogui.keyDown('t')
                time.sleep(np.random.uniform(0.3,0.7))        
                pyautogui.keyUp('t')
                time.sleep(np.random.uniform(0.3,0.7))
                
                time.sleep(2)

                break



def dailyLogin():
    #if daily reward is on screen, click accept
    try:
        location = pyautogui.locateCenterOnScreen('DailyLoginReward.png', grayscale=True, confidence=0.8)
        if location is not None:

            print("Daily reward is on screen, collecting.")
            #claim coordinates
            click(1164,937)
            time.sleep(np.random.uniform(1,3))
        else:
            print("Image not found.")
    except pyautogui.ImageNotFoundException:
        print("Already collected daily reward.")

def menuWheel():
    menuTavern()
    for _ in range (4):
        time.sleep(np.random.uniform(0.1,0.2))
        pyautogui.keyDown('q')
        time.sleep(np.random.uniform(0.1,0.2))
        pyautogui.keyUp('q')

def underworld():
    for _ in range (2):
        time.sleep(np.random.uniform(0.1,0.2))
        pyautogui.keyDown('b')
        time.sleep(np.random.uniform(0.1,0.2))
        pyautogui.keyUp('b')

    for _ in range (15):
        time.sleep(np.random.uniform(0.3,0.6))
        pressEnter()
        time.sleep(np.random.uniform(0.3,0.6))


def arenaManager():

    for _ in range(3):
        pyautogui.keyDown('b')
        time.sleep(np.random.uniform(0.3,0.7))        
        pyautogui.keyUp('b')
        time.sleep(np.random.uniform(0.3,0.7))  

    click(961,360)
    time.sleep(np.random.uniform(0.3,0.7))
    click(961,505)
    time.sleep(np.random.uniform(0.3,0.7))
    click(961,645)
    time.sleep(np.random.uniform(0.3,0.7))
    click(971,791)
    time.sleep(np.random.uniform(0.3,0.7))
    click(962,940)
    time.sleep(np.random.uniform(0.3,0.7))
    click(1730,352)
    time.sleep(np.random.uniform(0.3,0.7))
    click(1730,500)
    time.sleep(np.random.uniform(0.3,0.7))
    click(1730,650)
    time.sleep(np.random.uniform(0.3,0.7))
    click(1730,787)
    time.sleep(np.random.uniform(0.3,0.7))
    click(1730,938)
    time.sleep(np.random.uniform(0.3,0.7))

def dailyFreeWheel():
    #go to wheel and if its free, spin it
    menuWheel()
    time.sleep(2)

    try:
        location = pyautogui.locateCenterOnScreen('freeDailySpin.png', grayscale=True, confidence=0.8)
        if location is not None:
            
        #spin wheel coordinates
            click(644,1000)
            
            print("Free spin available. Spinning wheel")
        else:
            print("Image not found.")
    except pyautogui.ImageNotFoundException:
        print("Spinning the wheel is not free, moving on.")
        
    time.sleep(2)


def checkLogout():
    try:
        logoutCheck = pyautogui.locateCenterOnScreen('characterSelection.png', grayscale=True, confidence=0.8)
        if logoutCheck is not None:
            
        #spin wheel coordinates
            pressEnter()
            click(680,267)
            click(991,569)
            print("Logout Screen detected, logging back in.")
        else:
            print("Image not found.")
    except pyautogui.ImageNotFoundException:
        print("Still logged in, moving on.")
    time.sleep(2)


#Script start

#missing mount check, need it to give quest start a small margin


dailyLogin() #claims daily reward
dailyFreeWheel() #spins daily free wheel
arenaManager() #automated arena manager
underworld() #underworld lure hero automated
menuTavern() #go to tavern button, uses T shortcut

#hold q to exit script, need to fix this later
#ALWAYS DELAY 2 SECONDS WHEN PRESSING MENUS or using click() in general, game is old and slow
try:

    while True:

        checkLogout() # checks if the game didnt log you out, happens because of steam once in a while
        checkThirst() # checks if character still has energy, if not drink beer and if still no energy after beer exits program
        identifyTavChar(allTavernChars) # finds quest character in the tavern
        tavernLoop() #Checks all quests, picks highest XP one, tracks timer and finishes fight after time is done
        time.sleep(0.1)
    

except KeyboardInterrupt:
    print('Script stopped by user.')
    exit()

