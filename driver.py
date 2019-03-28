#!/usr/bin/env python3
# Copyright Countryside Greenhouse

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import RPi.GPIO as GPIO
from pygame import mixer
import pygame
import time
import glob

GPIO.setmode(GPIO.BCM)

GPIO.setup(3, GPIO.IN)
GPIO.setup(5, GPIO.OUT)

# TODO: Move this to json config file
char_sound_dir = '/home/pi/git/cuspeak/media/driver/'
bootup_sound_file = '/home/pi/git/cuspeak/bootup.mp3'
curr_file_index = 0


def get_speak_button():
    status = GPIO.input(3)
    if status == 1:
        status = 0
    elif status == 0:
        status = 1
    return status


def play_sound_file(filename):
    mixer.music.load(filename)
    mixer.music.play()
    while mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def get_next_sound_file():
    global curr_file_index
    flist = glob.glob(char_sound_dir + '*.mp3')
    if curr_file_index >= len(flist):
        curr_file_index = 0
    ret_val = flist[curr_file_index]
    curr_file_index += 1
    return ret_val


# Startup
pygame.init()
mixer.init()
play_sound_file(bootup_sound_file)

last_file = ''
try:
    while True:
        time.sleep(0.05)
        GPIO.output(5, 0)
        status = get_speak_button()
        # print("button status: {}".format(status))
        if status == 1:
            next_file = get_next_sound_file()
            GPIO.output(5, 1)  # Power on to AC unit
            # print("playing {}".format(next_file))
            play_sound_file(next_file)
            last_file = next_file
finally:
    GPIO.cleanup()
