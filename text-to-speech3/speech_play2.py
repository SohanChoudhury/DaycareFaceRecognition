# program to play appropriate audio clip when an individual is recognized
# with current version, program itself must be in same directory as audio clips
# association of clip index to individual recognized:
    # 1 = eddie
    # 2 = sohan
# this program will be called with argument for selection being the string name
# representation of the recognized individual


import os
import pygame



files = []



def myMain(person):

    loadClips()

    selection(person)



def selection(person):

    if person == "eddie":
        print("Eddie text selected")
        playClip(0)
        playClip(1)
        print("Eddie text spoken")
    elif person == "sohan":
        print("Sohan text selected")
        playClip(0)
        playClip(2)
        print("Sohan text spoken")
    else:
        print("No text selected")


def loadClips():

    for filename in os.listdir("./"):  # can specify a directory path here
        if filename.endswith(".wav"):
            files.append(filename)

    files.sort() # will be sorted in name order


    pygame.mixer.init()


def playClip(clip_index):


    pygame.mixer.music.load(files[clip_index])


    pygame.mixer.music.play()


    while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(1)



myMain("eddie")
# myMain("sohan") 
