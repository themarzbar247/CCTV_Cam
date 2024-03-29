import cv2
from subprocess_wrapper import send
import randomcolor
from collections import defaultdict
from camera_handler import camera
from commands import Recognise
import sys
import numpy as np
from pprint import pformat
def main(streaming_dir, camera_name, camra_path_url, cascadeClassifierPath):
    """The subproccess to wrapper that wraps around the live stream and handels the proccessing of individual frames via CV2 and write out to a livestream file. 

    Args:
        streaming_dir (String): Path like String for where the camera livestreams are going to be written to.
        camera_name (String): A human readable name for the camera i.e "Main Door 1"
        camra_path_url (String): The hosted camera livestream url that needs to be read in
        cascadeClassifierPath (String): A path like String of the Classifier that is wanted to be used to render the User Livestream
    """
    faceCascade = cv2.CascadeClassifier(cascadeClassifierPath)
    rand_color = randomcolor.RandomColor()
    next_color = lambda: [int(x) for x in rand_color.generate(luminosity='bright', format_='rgb')[0][4:-1].split(',')] 
    colors = defaultdict(next_color)
    with camera(streaming_dir, camera_name, camra_path_url) as camera_feed:
        while camera_feed.is_open():
            rect, frame = camera_feed.get_frame()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = [list(face)+[i] for i,face in enumerate(faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            ))]
            
            for (x, y, w, h, i) in faces:
                r = Recognise(frame, x, y, w, h, camera_name, gray[y:y+h,x:x+w])
                with open("t.txt", "a+") as f:
                    f.write(pformat(r))
                send(r)
  
            # Draw a rectangle around the faces
            for (x, y, w, h, i) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), colors[i] , 2)

            camera_feed.write_frame(frame)


if __name__=="__main__":
    main(*sys.argv[1:])