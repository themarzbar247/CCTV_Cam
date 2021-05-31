from pprint import pformat

class Command:
    def  __repr__(self):
        return f"{self.__name__}: {pformat(self.__dict__)}"

class Retrain(Command):
    def __init__(self,retrain_yml_path):
        super().__init__()
        self.trainer_path=retrain_yml_path
        
class Recognise(Command):
    def __init__(self, frame, x,y,w,h, camera, face):
        super().__init__()
        self.frame=frame
        self.face_rect = ((x, y), (w, h))
        self.camera = camera_name
        self.face=face
        
class Quit(Command):
    def __init__(self, data):
        super().__init__(data)
        
class Decide(Recognise):
    def __init__(self, frame, face_rect, camera, face, face_id, confidence):
        super().__init__( frame, face_rect, camera, face)
        self.face_id =face_id
        self.confidence = confidence

    @classmethod
    def create_from_get_frame(cls, getframe_command :Recognise, face_id, confidence):
        return cls(face_id=face_id, confidence=confidence, **getframe_command.__dict__)