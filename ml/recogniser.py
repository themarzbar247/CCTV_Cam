import cv2
from time import time
import sys
import threading
from subprocess_wrapper import recieve, send
from commands import Recognise, Retrain, Quit, Decide
import json

def main():
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
    recognizer = None

    def run(self, trainer_path, name_path):
        self.name_path = name_path
        self.trainer_path = trainer_path
        thread = threading.Thread(target=self.retrain, daemon=True)
        thread.start()

    def retrain(self):
        with open(self.name_path, "r") as f:
            self.names = json.load(f)
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer = recognizer.read(self.trainer_path)


if __name__ == "__main__":
    main(*sys.argv[1:])
