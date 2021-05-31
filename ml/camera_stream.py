import cv2
from subprocess_wrapper import send
import randomcolor
from collections import defaultdict
from camera_handler import camera
from commands import Recognise

def main(streaming_dir, camera_name, camra_path_url):
    rand_color = randomcolor.RandomColor()
    next_color = lambda: [int(x) for x in rand_color.generate(luminosity='bright', format_='rgb')[0][4:-1].split(',')] 
    colors = defaultdict(next_color)
    with camera(streaming_dir, camera_name, camra_path_url) as camera_feed:
        while camera_feed.is_open():
            rect, frame = camera_feed.get_frame()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = [list(face)+[i] for i,faces in enumerate(faceCascade) for face in faces.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )]
            
            for (x, y, w, h, i) in faces:
                send(Recognise(frame, x, y, w, h, camera_name, gray[y:y+h,x:x+w]))
  
            # Draw a rectangle around the faces
            for (x, y, w, h, i) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), colors[i] , 2)

            camera_feed.write_frame(frame)


if __name__=="__main__":
    main(*sys.argv[1:])