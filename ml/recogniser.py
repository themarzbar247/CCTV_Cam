import cv2
from time import time
import sys
import threading
from .helper.subprocess_wrapper import recieve,send


def main():
    retrainer = Retrainer()
    running = True
    while running:
        req = recieve()
        command=req["command"]
        data=req["data"]
        if command == "quit":
            running = False
        elif comand == "frame":
            face_id, confidence = retrainer.recognizer.predict(data["face"]) 
            data["face_id"] = face_id
            data["confidence"] = confidence
        elif comand == "retrain":
            retrainer.run(data["trainer_path"])
        send(req)


class Retrainer:
    recognizer = None

    def run(self, trainer_path=None):
        if trainer_path is not None:
            self.trainer_path = trainer_path
            thread = threading.Thread(target=self.retrain, daemon=True)
            thread.start()

    def retrain(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer = recognizer.read(self.train_yml_path)

if __name__ == "__main__":
    main(*sys.argv[1:])