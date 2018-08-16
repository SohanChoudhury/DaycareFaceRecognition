from playsound import playsound
import os

files = []

def selection(person):

    loadSound()

    if person == "eddie":
        playsound(files[0])
        playsound(files[1])
    elif person == "sohan":
        playsound(files[0])
        playsound(files[2])



def loadSound():
    for filename in os.listdir("/Users/schoudhury/openface/demos"):  # can specify a directory path here
        print(filename)
        if filename.endswith(".wav"):
            files.append(filename)

    files.sort()


# selection("eddie")
# selection("sohan")