from subprocess_wrapper import SubprocessWrapper
from recogniser import __file__ as recogniser_file
from camera_stream import __file__ as camera_stream_file
from recognizer_training_manager import __file__ as recognizer_training_manager_file
import json
from commands import Recognise, Decide,Retrain
import sys

def make_camera(streaming_dir, camera_name, camra_path_url):
    return SubprocessWrapper(camera_stream_file).start(streaming_dir, camera_name, camra_path_url)
    


def main(manager_config_file,camera_config_file):
    with  open(manager_config_file) as fp:
        manager_config = json.load(fp)
    with  open(camera_config_file) as fp:
        camera_config = json.load(fp)
    start_manager(camera_config= camera_config, **manager_config)
    


def start_manager(new_find_dir, data_set_dir, unknown_threshold, known_threshold,camera_config):
    cameras = []
    for camera in camera_config:
            cameras.append(make_camera(**camera))
    recogniser = SubprocessWrapper(recogniser_file).start()
    recognizer_training_manager = SubprocessWrapper(recognizer_training_manager_file).start(new_find_dir, data_set_dir).start()
    while True:
        for cam in cameras:
            face_command = cam.read() 
            if isinstance(face_command, Recognise):
                recogniser.send(face_command)
        recogniser_command = recogniser.read()
        if isinstance(recogniser_command,Decide):
            if recogniser_command.confidence <= unknown_threshold:
                pass
            elif recogniser_command.confidence >= known_threshold:
                pass
        training_command = recognizer_training_manager.read()
        if isinstance(training_command, Retrain):
            recogniser.send(training_command)

            








if __name__ == "__main__":
    main(*sys.argv[1:])