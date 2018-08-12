# program to play appropriate audio clip when an individual is recognized
# with current version, program itself must be in same directory as audio clips
# association of clip index to individual recognized:
    # 0 = eddie
    # 1 = sohan
# this program will be called with argument for processing being the string name
# representation of the recognized individual


import os
import pygame
import time



files = []


def myMain():

    loadClips()

    processing("eddie")
    # processing("sohan")


def processing(person):

    if person == "eddie":
        playClip(0)
    elif person == "sohan":
        playClip(1)
    else:
        print("No go")


def loadClips():

    for filename in os.listdir():  # can specify a directory path here
        if filename.endswith(".mp3"):
            files.append(filename)

    files.sort() # will be sorted in name order


    pygame.mixer.init()


def playClip(clip_index):


    pygame.mixer.music.load(files[clip_index])


    pygame.mixer.music.play()
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(1)

    print("hi")


myMain()