from subprocess_wrapper import SubprocessWrapper
from recogniser import __file__ as recogniser_file
from camera_stream import __file__ as camera_stream_file
from recognizer_training_manager import __file__ as recognizer_training_manager_file
import json
from commands import Recognise, Decide,Retrain
import sys
from recognizer_training_manager import filename_collision_resolve
from time import time
from os.path import join

def make_camera(streaming_dir, camera_name, camra_path_url, cascadeClassifierPath):
    """Takes config for a camera and builds a camera subprocess from the config


    Args:
        streaming_dir (String): Path like String for where the camera livestreams are going to be written to.
        camera_name (String): A human readable name for the camera i.e "Main Door 1"
        camra_path_url (String): The hosted camera livestream url that needs to be read in 
        cascadeClassifierPath (String): A path like String of the Classifier that is wanted to be used to render the User Livestream

    Returns:
       SubprocessWrapper : A camera subproccess wrapper to handel the various processes that run on an individual camera.
    """
    return SubprocessWrapper(camera_stream_file).start(streaming_dir, camera_name, camra_path_url,cascadeClassifierPath)
    


def main(manager_config_file,camera_config_file):
    """[summary]

    Args:
        manager_config_file ([type]): [description]
        camera_config_file ([type]): [description]
    """
    with  open(manager_config_file) as fp:
        manager_config = json.load(fp)
    with  open(camera_config_file) as fp:
        camera_config = json.load(fp)
    start_manager(camera_config= camera_config, **manager_config)
    


def start_manager(alert_dir, new_find_dir, data_set_dir, unknown_threshold, known_threshold, cascadeClassifierPath, camera_config):
    """Starts all the Camera proccesses and Recogniser proccess and a Training model proccess, this is the Top level function and is were each of the commands are initilised from. 

    Args:
        alert_dir (String): A path like String where all alert infomation will be stored i.e The frame with the unknown face in.
        new_find_dir (String): A path like String of where new found images used for training should be stored.
        data_set_dir (String): A path like String of the training dataset
        unknown_threshold (Int): A number repersenting the percentage confidance score as an upper bound to alert on unknown people 
        known_threshold (Int): A number repersenting the percentage confidance score as an lower bound to alert on known people
        cascadeClassifierPath (String): A path like String of the Classifier that is wanted to be used to render the User Livestream.
        camera_config (String):  A path like String to the camera config file.
    """
    cameras = []
    for camera in camera_config:
            cameras.append(make_camera(cascadeClassifierPath=cascadeClassifierPath, **camera))
    recogniser = SubprocessWrapper(recogniser_file).start()
    recognizer_training_manager = SubprocessWrapper(recognizer_training_manager_file).start(new_find_dir, data_set_dir)
    
    while True:
        training_command = recognizer_training_manager.read()
        if isinstance(training_command, Retrain):
            recogniser.send(training_command)
        for cam in cameras:
            face_command = cam.read() 
            if isinstance(face_command, Recognise):
                recogniser.send(face_command)
        recogniser_command = recogniser.read()
        if isinstance(recogniser_command,Decide):
            if recogniser_command.confidence <= unknown_threshold:
                print("found a face with less than {recogniser_command.confidence} confidence")
                t = time()
                cv2.imwrite(filename_collision_resolve(join(alert_dir, f"{t}_frame.jpg")),recogniser_command.frame)
                cv2.imwrite(filename_collision_resolve(join(alert_dir, f"{t}_face.jpg")),recogniser_command.face)
            elif recogniser_command.confidence >= known_threshold:
                cv2.imwrite(filename_collision_resolve(join(new_find_dir, recogniser_command.name, f"{t}.jpg")),recogniser_command.face)

            








if __name__ == "__main__":
    main(*sys.argv[1:])