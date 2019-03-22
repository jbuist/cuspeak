#!/usr/bin/python
# Copyright Countryside Greenhouse

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import RPi.GPIO as GPIO
from pygame import mixer
import pygame

GPIO.setmode(GPIO.BCM)

# Appearntly not needed for IO3.. go fig.
#GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(3, GPIO.IN)
GPIO.setup(5, GPIO.OUT)

def getSpeakButton():
    status = GPIO.input(3)
    if status == 1:
        status = 0
    elif status == 0:
        status = 1
    return status

def playSoundFile(filename):
    mixer.music.load(filename)
    mixer.music.play()
    while mixer.music.get_busy():
        pygame.time.Clock().tick(10)


# Startup
pygame.init()
mixer.init()
playSoundFile("/opt/cside/bin/bootup.mp3")

while True:
    GPIO.output(5, 0)
    status = getSpeakButton()
    #print status
    if status == 1:
        GPIO.output(5, 1)
        #playSoundFile("/opt/cside/bin/lawman_nocash.mp3")






