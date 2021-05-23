import cv2
import sys
import random


faceCascade = [cv2.CascadeClassifier(x) for x in sys.argv[1:]]

video_capture = cv2.VideoCapture('http://192.168.1.100:8080/camera/livestream.m3u8')
colors = [(random.randint(0,255), random.randint(0,255), random.randint(0,255)) for i in faceCascade]

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    print(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    faces = [list(face)+[i] for i,faces in enumerate(faceCascade) for face in faces.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )]

    # Draw a rectangle around the faces
    for (x, y, w, h, i) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), colors[i], 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()