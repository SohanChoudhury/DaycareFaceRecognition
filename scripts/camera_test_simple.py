# import numpy as np
# import cv2

# cap = cv2.VideoCapture("http://192.168.86.31/dms?nowprofileid=1&0.10957443734292038")

# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     # Our operations on the frame come here
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Display the resulting frame
#     cv2.imshow('frame',frame)
#     cv2.imshow('gray',gray)
#     if cv2.waitKey(20) & 0xFF == ord('q'):
#         break

# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()


# import numpy as np
# import cv2

# cap = cv2.VideoCapture("http://admin:supple123@192.168.86.35/mjpeg.cgi")

# while(True):
#     ret, frame = cap.read()
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



# import numpy as np
# import cv2
# cap = cv2.VideoCapture()
# cap.open("http://admin:supple123@192.168.86.35/mjpeg.cgi")

# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     # Our operations on the frame come here
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Display the resulting frame
#     cv2.imshow('frame',gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#           break

#    # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()



# import numpy as np
# import cv2

# cap = cv2.VideoCapture(0)

# while(True):
#     ret, frame = cap.read()
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


# below block is to test IP camera!!!

import cv2
import requests
import numpy as np

r = requests.get('http://192.168.86.35/mjpeg.cgi', auth=('admin', 'supple123'), stream=True)

bytes = bytes()
for chunk in r.iter_content(chunk_size=1024):
    bytes += chunk
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]

        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()



# import cv2
# import requests
# import numpy as np

# r = requests.get('http://192.168.86.35/mjpeg.cgi', auth=('admin', 'supple123'), stream=True)

# bytes = bytes()

# for chunk in r.iter_content(chunk_size=1024):
#     bytes += chunk
#     a = bytes.find(b'\xff\xd8')
#     b = bytes.find(b'\xff\xd9')
#     if a != -1 and b != -1:
#         jpg = bytes[a:b+2]
#         bytes = bytes[b+2:]

#         frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
#         cv2.imshow("frame", frame)






# confidenceList = []

# r = requests.get('http://192.168.86.35/mjpeg.cgi', auth=('admin', 'supple123'), stream=True)
# bytes = bytes()

# for chunk in r.iter_content(chunk_size=1024):

#     bytes += chunk
#     a = bytes.find(b'\xff\xd8')
#     b = bytes.find(b'\xff\xd9')
#     if a != -1 and b != -1:
#         jpg = bytes[a:b+2]
#         bytes = bytes[b+2:]

#         frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

#     persons, confidences, bbs = infer(frame, args)
#     print ("P: " + str(persons) + " C: " + str(confidences))
#     try:
#         # append with two floating point precision
#         confidenceList.append('%.2f' % confidences[0])
#     except:
#         # If there is no face detected, confidences matrix will be empty.
#         # We can simply ignore it.
#         pass

#     for i, c in enumerate(confidences):
#         if c <= args.threshold:  # 0.5 is kept as threshold for known face.
#             persons[i] = "_unknown"

#     # Print the person name and conf value on the frame next to the person
#     # Also print the bounding box
#     for idx,person in enumerate(persons):
#         cv2.rectangle(frame, (bbs[idx].left(), bbs[idx].top()), (bbs[idx].right(), bbs[idx].bottom()), (0, 255, 0), 2)
#         cv2.putText(frame, "{} @{:.2f}".format(person, confidences[idx]),
#                     (bbs[idx].left(), bbs[idx].bottom()+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

#     cv2.imshow('frame', frame)
#     # quit the program on the press of key 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# # When everything is done, release the capture
# cv2.destroyAllWindows()





