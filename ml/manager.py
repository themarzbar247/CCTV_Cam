
from .helper.subprocess_wrapper import SubprocessWrapper
from recogniser import __file__ as recogniser_file
from camera_stream import __file__ as camera_stream_file
from recognizer_training_manager import __file__ as recognizer_training_manager_file
import json

def make_camera(streaming_dir, camera_name, camra_path_url):
    return SubprocessWrapper(camera_stream_file).start(streaming_dir, camera_name, camra_path_url)
    


def main(new_find_dir, data_set_dir, camera_config_file):
    recogniser = SubprocessWrapper(recogniser_file).start()
    recognizer_training_manager = SubprocessWrapper(recognizer_training_manager_file).start(new_find_dir, data_set_dir).start()
    cameras = []
    with  open(camera_config_file) as fp:
        for camera in json.load(fp):
            cameras.append(make_camera(*camera))
    while True:
        for cam in cameras:
            face_command = cam.read() 
            if face_command is not None:
                recogniser.send(face_command)
        recogniser_command = recogniser.read()
        if recogniser_command is not None:
            pass
            """
            this is where we know about the frame and face and who we think it is with a confidence level.
            """
        training_command = recognizer_training_manager.read()
        if training_command is not None:
            recogniser.send(training_command)

            








if __name__ == "__main__":
    main(*argv[:1])