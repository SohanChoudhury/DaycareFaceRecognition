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

    elif person == "mohua":
        print("Mohua text selected")
        playClip(0)
        playClip(3)
        print("Mohua text spoken")
    elif person == "fatema":
        print("Fatema text selected")
        playClip(0)
        playClip(4)
        print("Fatema text spoken")

    elif person == "drena-mom":
        print("Drena mom text selected")
        playClip(0)
        playClip(5)
        print("Drena mom text spoken")
    elif person == "ojas-mom":
        print("Ojas mom text selected")
        playClip(0)
        playClip(6)
        print("Ojas mom text spoken")

    else:
        print("No text selected")


def loadClips():

    for filename in os.listdir("/Users/schoudhury/openface/demos"):  # can specify a directory path here
        if filename.endswith(".ogg"):
            files.append(filename)

    files.sort() # will be sorted in name order


    # pygame.init()
    pygame.mixer.init() # problem?


def playClip(clip_index):

    print(files)
    print(clip_index)


    pygame.mixer.music.load("/Users/schoudhury/openface/demos/" + files[clip_index]) # problem


    pygame.mixer.music.play()


    while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(1)



# selection("eddie")
# selection("sohan")
