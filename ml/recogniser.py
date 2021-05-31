import cv2
from time import time
import sys
import threading
from subprocess_wrapper import recieve,send
from commands import Recognise, Retrain, Quit, Decide

def main():
    retrainer = Retrainer()
    running = True
    while running:
        command = recieve()
        if isinstance(command,Quit):
            running = False
        elif isinstance(command,Recognise):
            face_id, confidence = retrainer.recognizer.predict(command.face) 
            command = Decide.create_from_get_frame(command, face_id, confidence)
        elif isinstance(command,Retrain):
            retrainer.run(command.trainer_path)
        send(command)

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