import sys
import subprocess
import cv2
import ffmpeg
import numpy as np
import os
import queue
import time
from threading  import Thread


# TODO: using threading read from stin and add to queue to be used as commands for the control of a stream.
# sub use this module to subprocess the camera and run it indipendantly
# set up a retrain command that will rerun the trainer
# set up a threshold comand that will save on high threshold for future training
# set up a low threashold and similar to create alerts off of ans ssave
# lable and output faces.


def main(camra_path_url, camera_name, streaming_dir="./cctvCamera/cctv/static"):
    
    with camera(streaming_dir, camera_name, camra_path_url) as camera_feed:
        while camera_feed.is_open():
            rect, frame = camera_feed.get_frame()
            # process
            camera_feed.write_frame(frame)


# In my mac webcamera is 0, also you can set a video file name instead, for example "/home/user/demo.mp4"
#path = 'http://192.168.1.100:8080/camera/livestream.m3u8'


# command and params for ffmpeg


class camera:

    def __init__(self, streaming_dir, out_dir_name, in_url):
        self.streaming_dir = streaming_dir
        self.out_dir_name = out_dir_name
        self.in_url = in_url
        self.cap=None

    def get_camera_output_dir(self):
        return os.path.join(self.streaming_dir,self.out_dir_name)

    def is_open(self): return self.cap.isOpened() if self.cap is not None else False

    def start_ffmpeg_output_stream(self):
        args = (
            ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(self.width, self.height))
            .output(
                os.path.join(self.get_camera_output_dir(), "stream.m3u8"),
                hls_flags="delete_segments",
                segment_list_flags="+live",
                pix_fmt='yuv420p')
            .overwrite_output()
            .compile()
        )
        return subprocess.Popen(
            args, stdin=subprocess.PIPE, shell=True)

    def write_frame(self, frame):
        if not self.is_open():
            raise Exception("Error: input not open")
        self.out_stream.stdin.write(
            frame
            .astype(np.uint8)
            .tobytes()
        )

    def get_frame(self, timeout=10):
        if not self.is_open():
            raise Exception("Error: input not open")
        t = time.time()
        r,f = self.cap.read()
        while not r and time.time()-t < timeout:
            r,f = self.cap.read()
        return r,f

    def start_camera(self):
        cap = cv2.VideoCapture(self.in_url)
        self.fps = int(cap.get(cv2.CAP_PROP_FPS))
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        os.makedirs(self.get_camera_output_dir(), exist_ok=True)
        self.out_stream = self.start_ffmpeg_output_stream()
        self.cap = cap
        self.get_frame(timeout=60)


    def __enter__(self):
        self.start_camera()
        return self

    def __exit__(self, type, value, traceback):
        self.dispose()

    def dispose(self):
        self.out_stream.stdin.close()
        self.out_stream.wait()


if(__name__ == "__main__"):
    main(*sys.argv[1:])
