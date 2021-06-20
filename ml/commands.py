from pprint import pformat

class Command:
    def  __repr__(self):
        return f"command - {pformat(self.__dict__)}"

class Retrain(Command):
    def __init__(self,retrain_yml_path, name_file, wait=False):
        super().__init__()
        self.trainer_path=retrain_yml_path
        self.name_path = name_file
        self.wait=wait
        
class Recognise(Command):
    def __init__(self, frame, x,y,w,h, camera_name, face):
        super().__init__()
        self.frame=frame
        self.face_rect = ((x, y), (w, h))
        self.camera = camera_name
        self.face = face
        
class Quit(Command):
    def __init__(self, data):
        super().__init__(data)
        
class Decide(Recognise):
    def __init__(self, frame, face_rect, camera, face, face_id, name, confidence):
        super().__init__( frame, face_rect, camera, face)
        self.face_id =face_id
        self.confidence = confidence
        self.name = name

    @classmethod
    def create_from_get_frame(cls, getframe_command :Recognise, face_id, name, confidence):
        return cls(face_id=face_id, confidence=confidence, name=name, **getframe_command.__dict__)