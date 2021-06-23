import cv2
from time import time
import sys
import threading
from subprocess_wrapper import recieve, send
from commands import Recognise, Retrain, Quit, Decide
import json

def main():
    """Handles Commands passed to this subprocess and returns an assesed image, either to retrain the model or recognise on a frame. Result gets 
    """
    retrainer = Retrainer()
    running = True
    while running:
        command = recieve()
        if isinstance(command, Quit):
            running = False
        elif isinstance(command, Recognise):
            face_id, confidence = retrainer.recognizer.predict(command.face)
            name = retrainer.names[face_id]
            command = Decide.create_from_get_frame(command, face_id, name, confidence)
        elif isinstance(command, Retrain):
            retrainer.run(command.trainer_path, command.name_path)
            while command.wait and retrainer.recognizer is None:
                pass
        send(command)


class Retrainer:
    """It a class to handel the hand over to the retrained model and maintain coverage while the swap it happening.
    """
    recognizer = None

    def run(self, trainer_path, name_path):
        """Initalises the hand over thread

        Args:
            trainer_path (String): Path like String pointing to the current trainer.yml
            name_path (String): Path like String pointing to the names.json file.
        """
        self.name_path = name_path
        self.trainer_path = trainer_path
        thread = threading.Thread(target=self.retrain, daemon=True)
        thread.start()

    def retrain(self):
        """Starts the retaining subproccess for use in the hand over thread
        """
        with open(self.name_path, "r") as f:
            names = json.load(f)
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer = recognizer.read(self.trainer_path)
        self.names = names


if __name__ == "__main__":
    main(*sys.argv[1:])
