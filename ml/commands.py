from pprint import pformat

class Command:
    """Class to handle the different types of commands. 
    """
    def  __repr__(self):
        return f"command - {pformat(self.__dict__)}"

class Retrain(Command):
    """This is the command to handel the signals to retrain the model. Holds infomation about how to retrain. 

    Args:
        Retrain(Command) : Command method that can be used to pass messages between the trining manager and the recogniser. 
    """
    def __init__(self,retrain_yml_path, name_file, wait=False):
        super().__init__()
        self.trainer_path=retrain_yml_path
        self.name_path = name_file
        self.wait=wait
        
class Recognise(Command):
    """This is the command to handel the signals to recognise a frame.

    Args:
        Recognise(Command) : Command method that can be used to pass messages between a camera and the recogniser.
    """
    def __init__(self, frame, x,y,w,h, camera_name, face):
        super().__init__()
        self.frame=frame
        self.face_rect = ((x, y), (w, h))
        self.camera = camera_name
        self.face = face
        
class Quit(Command):
    """This is the command to handel a end hook to a subprocess

    Args:
        Quit(Command) : Command method to hault a subprocess
    """
    def __init__(self, data):
        super().__init__(data)
        
class Decide(Recognise):
    """This is the command to handel the confidance score.

    Args:
        Decide(Recognise): Command method to pass messages between the recogniser and the manager to decide what to do given the confidance score.
    """
    def __init__(self, frame, face_rect, camera, face, face_id, name, confidence):
        super().__init__( frame, face_rect, camera, face)
        self.face_id =face_id
        self.confidence = confidence
        self.name = name

    @classmethod
    def create_from_get_frame(cls, getframe_command :Recognise, face_id, name, confidence):
        """Factory to convert from the subclass recogniser and the decide class.
        """
        return cls(face_id=face_id, confidence=confidence, name=name, **getframe_command.__dict__)