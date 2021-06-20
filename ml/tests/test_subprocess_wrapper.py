from child import __file__ as child
from ..subprocess_wrapper import SubprocessWrapper
from PIL import Image
import numpy as np

def test_passthough_small():
    p = SubprocessWrapper(child).start()
    PIL_image = Image.open("./small_image.jpg")
    arr = np.array(PIL_image,'uint8')
    p.send(arr)
    assert np.array_equal(p.read(True),arr)

def test_passthough_big():
    p = SubprocessWrapper(child).start()
    PIL_image = Image.open("./big_image.jpg")
    arr = np.array(PIL_image,'uint8')
    p.send(arr)
    assert np.array_equal(p.read(True),arr)
 
def test_passthough_exception():
    p = SubprocessWrapper(child).start()
    e = Exception("test exception")
    p.send(e)
    try:
        p.read(True)
    except Exception as e2:
        assert e == e2
