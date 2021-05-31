import subprocess
import sys
from child import __file__ as child
from subprocess_wrapper import SubprocessWrapper
from PIL import Image
import numpy as np


p = SubprocessWrapper(child).start()
PIL_image = Image.open("C:\\Users\\myles\\Documents\\project\\CCTV_Cam\\CCTV_Cam\\1b55e4bdb4fc6051382e370bf26d5a59.jpg")
#PIL_image = Image.open("C:\\Users\\myles\\Documents\\project\\CCTV_Cam\\tmp_dataset\\Myles Puddephatt\\1DENmxn4_n.jpg")#"C:\\Users\\myles\\Documents\\project\\CCTV_Cam\\CCTV_Cam\\1b55e4bdb4fc6051382e370bf26d5a59.jpg")
arr = np.array(PIL_image,'uint8')
p.send(arr)
print(p.read(True)==np.array(PIL_image,'uint8'))

