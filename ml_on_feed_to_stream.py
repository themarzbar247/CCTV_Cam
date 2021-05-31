import subprocess
import cv2
import ffmpeg

import numpy as np
import sys
import os
# In my mac webcamera is 0, also you can set a video file name instead, for example "/home/user/demo.mp4"
path = 'http://192.168.1.100:8080/camera/livestream.m3u8'
cap = cv2.VideoCapture(path)

# gather video info to ffmpeg
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# command and params for ffmpeg


def start_ffmpeg_output_stream(out_filename, width, height):
    args = (
        ffmpeg
        .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
        .output(out_filename,hls_flags="delete_segments",segment_list_flags="+live", pix_fmt='yuv420p')
        .overwrite_output()
        .compile()
    )
    print(args)
    return subprocess.Popen(args, stdin=subprocess.PIPE, shell=True)


def write_frame(out_stream, frame):
    x = frame.astype(np.uint8).tobytes()
    out_stream.stdin.write(x)


s = start_ffmpeg_output_stream(os.path.join(sys.argv[-1],"stream.m3u8"), width, height)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("frame read failed")
        continue

    # YOUR CODE FOR PROCESSING FRAME HERE

    # write to pipe
    write_frame(s, frame)
s.stdin.close()
s.wait()
