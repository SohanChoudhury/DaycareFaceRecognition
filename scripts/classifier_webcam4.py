#!/usr/bin/env python2



import time

start = time.time()

import argparse
import cv2
import os
import pickle
import sys

import requests
import time

import numpy as np
np.set_printoptions(precision=2)
from sklearn.mixture import GMM
import openface


import speech_play2 as speech
# import speech_play3 as speech

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, '..', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')


def getRep(bgrImg):
    start = time.time()
    if bgrImg is None:
        raise Exception("Unable to load image/frame")

    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

    if args.verbose:
        print("  + Original size: {}".format(rgbImg.shape))
    if args.verbose:
        print("Loading the image took {} seconds.".format(time.time() - start))

    start = time.time()

    # Get the largest face bounding box
    # bb = align.getLargestFaceBoundingBox(rgbImg) #Bounding box

    # Get all bounding boxes
    bb = align.getAllFaceBoundingBoxes(rgbImg)

    if bb is None:
        # raise Exception("Unable to find a face: {}".format(imgPath))
        return None
    if args.verbose:
        print("Face detection took {} seconds.".format(time.time() - start))

    start = time.time()

    alignedFaces = []
    for box in bb:
        alignedFaces.append(
            align.align(
                args.imgDim,
                rgbImg,
                box,
                landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE))

    if alignedFaces is None:
        raise Exception("Unable to align the frame")
    if args.verbose:
        print("Alignment took {} seconds.".format(time.time() - start))

    start = time.time()

    reps = []
    for alignedFace in alignedFaces:
        reps.append(net.forward(alignedFace))

    if args.verbose:
        print("Neural network forward pass took {} seconds.".format(
            time.time() - start))

    # print (reps)
    return (reps,bb)


def infer(img, args):
    with open(args.classifierModel, 'r') as f:
        if sys.version_info[0] < 3:
                (le, clf) = pickle.load(f)  # le - label and clf - classifer
        else:
                (le, clf) = pickle.load(f, encoding='latin1')  # le - label and clf - classifer

    repsAndBBs = getRep(img)
    reps = repsAndBBs[0]
    bbs = repsAndBBs[1]
    persons = []
    confidences = []
    for rep in reps:
        try:
            rep = rep.reshape(1, -1)
        except:
            print ("No Face detected")
            return (None, None)
        start = time.time()
        predictions = clf.predict_proba(rep).ravel()
        # print (predictions)
        maxI = np.argmax(predictions)
        # max2 = np.argsort(predictions)[-3:][::-1][1]
        persons.append(le.inverse_transform(maxI))
        # print (str(le.inverse_transform(max2)) + ": "+str( predictions [max2]))
        # ^ prints the second prediction
        confidences.append(predictions[maxI])
        if args.verbose:
            print("Prediction took {} seconds.".format(time.time() - start))
            pass
        # print("Predict {} with {:.2f} confidence.".format(person.decode('utf-8'), confidence))
        if isinstance(clf, GMM):
            dist = np.linalg.norm(rep - clf.means_[maxI])
            print("  + Distance from the mean: {}".format(dist))
            pass
    return (persons, confidences ,bbs)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dlibFacePredictor',
        type=str,
        help="Path to dlib's face predictor.",
        default=os.path.join(
            dlibModelDir,
            "shape_predictor_68_face_landmarks.dat"))
    parser.add_argument(
        '--networkModel',
        type=str,
        help="Path to Torch network model.",
        default=os.path.join(
            openfaceModelDir,
            'nn4.small2.v1.t7'))
    parser.add_argument('--imgDim', type=int,
                        help="Default image dimension.", default=96)
    parser.add_argument(
        '--captureDevice',
        type=int,
        default=0,
        help='Capture device. 0 for latop webcam and 1 for usb webcam')
    parser.add_argument('--width', type=int, default=320)
    parser.add_argument('--height', type=int, default=240)
    parser.add_argument('--threshold', type=float, default=0.6)
    parser.add_argument('--cuda', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument(
        'classifierModel',
        type=str,
        help='The Python pickle representing the classifier. This is NOT the Torch network model, which can be set with --networkModel.')

    args = parser.parse_args()

    align = openface.AlignDlib(args.dlibFacePredictor)
    net = openface.TorchNeuralNet(
        args.networkModel,
        imgDim=args.imgDim,
        cuda=args.cuda)

    # Capture device. Usually 0 will be webcam and 1 will be usb cam.
    # video_capture = cv2.VideoCapture(args.captureDevice)
    # video_capture.set(3, args.width)
    # video_capture.set(4, args.height)

    confidenceList = []

    r = requests.get('http://192.168.86.35/mjpeg.cgi', auth=('admin', 'supple123'), stream=True)
    bytes = bytes()


    person_detected = False
    detected_people = []

    detection_times = {"eddie":0, "sohan":0, "mohua":0, "fatema":0, "drena-mom":0, "ojas-mom":0}


    for chunk in r.iter_content(chunk_size=1024):

        bytes += chunk
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]

            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            image_captured_time = time.time()

            persons, confidences, bbs = infer(frame, args)
            print ("P: " + str(persons) + " C: " + str(confidences))


            if len(persons) > 0 and not person_detected:
                speech.loadClips()

                person_detected = True

            if len(persons) > 0:
                detection_captured_time = time.time()


            for person in persons:

                processing_time = detection_captured_time - image_captured_time

                if detection_times[person] > 0 and processing_time < detection_times[person]:

                    detection_times[person] = processing_time

                elif detection_times[person] == 0:

                    detection_times[person] = processing_time

                if person not in detected_people:

                    speech.selection(person)


                    detected_people.append(person)

            print(detection_times)


            try:
                # append with two floating point precision
                confidenceList.append('%.2f' % confidences[0])

            except:
                # If there is no face detected, confidences matrix will be empty.
                # We can simply ignore it.
                # print ("P: []" + " C: []")
                pass

            for i, c in enumerate(confidences):
                if c <= args.threshold:  # 0.5 is kept as threshold for known face.
                    persons[i] = "_unknown"

            # Print the person name and conf value on the frame next to the person
            # Also print the bounding box
            for idx,person in enumerate(persons):
                cv2.rectangle(frame, (bbs[idx].left(), bbs[idx].top()), (bbs[idx].right(), bbs[idx].bottom()), (0, 255, 0), 2)
                cv2.putText(frame, "{} @{:.2f}".format(person, confidences[idx]),
                            (bbs[idx].left(), bbs[idx].bottom()+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            cv2.imshow('frame', frame)
            # quit the program on the press of key 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    # When everything is done, release the capture
    cv2.destroyAllWindows()