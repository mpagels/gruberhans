#!/usr/bin/python

# Attention! Bad language in this code!

import pygame
import random
import time
import threading
import RPi.GPIO as GPIO
from gpiozero import Button
from gpiozero import PWMLED


def change_lang_path(language):
    
    '''Function to change the path to the mp3 files.'''

    global language_status_led
    global path
    
    if language == "en":
        language_status_led.value = 0
        path = "/home/pi/Desktop/weihnachten/en/"
        path_list = [path+"asskick.mp3", path+"same_shit.mp3", path+"normal_christmas.mp3"]
    else:
        language_status_led.value = 0.5
        path = "/home/pi/Desktop/weihnachten/de/"
        path_list = [path+"asskick.mp3", path+"same_shit.mp3", path+"normal_christmas.mp3"]
    
    return path_list

def change_lang():
    
    '''Function to change the language after pressing button
    connected to PIN 2. (German to english and back)'''

    global language
    global path
    global path_list
    
    while True:
        language_button.wait_for_press()
        if language == "de":
            language = "en"
            path_list = change_lang_path(language)
            time.sleep(1)
        else:
            language = "de"
            path_list = change_lang_path(language)
            time.sleep(1)
        
    
def lighter_light():

    '''Function to simulate the lighter light'''
    
    global lighter
    
    while True:
        lighter.value =(round(random.random(),1))
        time.sleep(0.05)
      
# PIN config
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)

language_button = Button(2)
lighter = PWMLED(21)
language_status_led = PWMLED(26)
language_status_led.value = 0.5

# Language config
path = "/home/pi/Desktop/weihnachten/de/"
path_list = [path+"asskick.mp3", path+"same_shit.mp3", path+"normal_christmas.mp3"]
language = "de"

pygame.init()  

# Setting and start thread for language change and lighter light
change_thread = threading.Thread(target=change_lang)
lighter_thread = threading.Thread(target=lighter_light)
lighter_thread.start()
change_thread.start()

# main loop
try:
    while True:
        # If PIN 20 pushed, choose from 0 or 1

        if GPIO.input(20) == True:
            
            random_input = random.choice([0,1])

            # if 1 play motherfucker.mp3 else chose one of the mp3s in path_list
            
            if random_input == 1:    
                sound = path+"motherfucker.mp3" 
            else:
                sound = random.choice(path_list)

            # use pygame to play the mp3 over the headphone jack
            
            pygame.mixer.music.load(sound)
            pygame.mixer.music.play()
            time.sleep(1)
            
except KeyboardInterrupt:
    GPIO.cleanup()
    language_status_led.close()
    lighter.close()
