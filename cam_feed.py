import cv2
import threading
from queue import Queue


class camera_feed:

    def __init__(self, url, max_size = 128):
        self.Q = Queue(maxsize=max_size)
        self.stream = cv2.VideoCapture(url)
        self.stream.set(3, 640) # set video widht
        self.stream.set(4, 480) # set video height# Define min window size to be recognized as a face
        self.minW = 0.1*self.stream.get(3)
        self.minH = 0.1*self.stream.get(4)
        self.running = False
    
    def min_size(self):
        return (int(minW), int(minH))

    def update(self):
        self.running=True
        while self.running:
            # Capture frame-by-frame
            if self.Q.full():
                self.Q.get_nowait()
            self.Q.put(self.stream.read())
            
    def get(self):
        if not self.running:
            raise Exception("feed not started")
        t= self.Q.get_nowait() 
        print(t)
        return t     
    
    def start(self):
        self.t = threading.Thread(target=self.update(),args=())
        self.t.daemon=True
        self.t.start()
        return self

    def stop(self):
        # indicate that the thread should be running
        self.running = False
        self.stream.release()

URL='http://192.168.1.100:8080/camera/livestream.m3u8'

