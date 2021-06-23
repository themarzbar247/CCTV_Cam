import threading
import os
import sys
import hashlib
import glob
import random
import shutil
import cv2
import json
from PIL import Image
import numpy as np
from subprocess_wrapper import send
from commands import Retrain
import sys

CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"

def filename_collision_resolve(img_path):
    """A function to ensure that the a new filename is unique.

    Args:
        img_path (String): A path like string related to the local file system.

    Returns:
        String: A path like sting that does not yet exist (not thread safe).
    """
    initial, ext = os.path.basename(img_path).split(os.extsep,1)
    while os.path.exists(img_path):
        fn = os.path.basename(img_path)
        new_name = "".join([random.choice(CHARSET) for _ in range(10)])
        img_path=img_path.replace(fn, f"{initial}({new_name}){os.extsep}{ext}")
    return img_path

def main(new_find_dir, data_set_dir, rebuild_threshold=10):
    """Proccess incharge of reading in new found images in batches and retraining a model with them.

    Args:
        new_find_dir (String): A path like string referanceing a directory conatining new images to train on.

        data_set_dir (String): A path like string referancing the original directory containing the orignal image training dataset.

        rebuild_threshold (int, optional): This is the number of images found in the 'new_find_dir' before it should retrain. Defaults to 10.
    """
    r = RecogniserTrainer(new_find_dir, data_set_dir, rebuild_threshold)
    #if we dont want to rebuild we need to tell others about the current file
    if r.should_rebuild():
        s = r.build_yml()
    send(Retrain(r.trainer_file,r.names_file,True))
    from time import sleep
    while True:
        if r.should_rebuild():
            r.copy_dataset_additions()
            traner_file,name_file = r.build_yml()
            send(Retrain(traner_file,name_file))
        sleep(30)



class RecogniserTrainer:
    """ This encapulates the CV2 model used to control retraining.
      Args:
        new_find_dir (String): A path like string referanceing a directory conatining new images to train on.

        data_set_dir (String): A path like string referancing the original directory containing the orignal image training dataset.

        rebuild_threshold (int, optional): This is the number of images found in the 'new_find_dir' before it should retrain. Defaults to 10.
   """
    def __init__(self, new_find_dir, data_set_dir, rebuild_threshold=10):
        self.rebuild_threshold=rebuild_threshold
        self.new_find_dir = new_find_dir
        self.data_set_dir = data_set_dir
        self.trainer_file = os.path.join(data_set_dir,"trainer.yml")
        self.names_file = os.path.join(data_set_dir,"names.json")

    def _get_new_img_paths(self):
        """This creates a list of .jpg files from the new found faces directory dataset and returns it.
        Returns:
            [String]: A list of newly found .jpg files.
        """
        return glob.glob(os.path.join(self.new_find_dir,"**\\*.jpg"))

    def _get_dataset_img_paths(self):
        """This creates a list of .jpg files from the orignial dataset and returns it.

        Returns:
            [String]: A list of the orignal training image dataset.
        """
        return glob.glob(os.path.join(self.data_set_dir,"**\\*.jpg"))

    def copy_dataset_additions(self):
        """Safly moves data from the new dataset (found images) into the original dataset directory resolving image name collisions as found.
        """
        new_imgs = self._get_new_img_paths()
        for img_path in new_imgs:
            new_path = img_path.replace(self.new_find_dir, self.data_set_dir)
            new_path = filename_collision_resolve(new_path)
            try:
                os.mkdir(os.path.dirname(new_path))
            except:
                pass
            shutil.copy(img_path, new_path)
            os.remove(img_path)
    
    def should_rebuild(self):
        """Checks to see if a retraining is required on the new dataset based on the threshold set.
        If the number of images is greater than the threshold or if there is no trainer file present return True else False

        Returns:
            Boolean
        """
        return len(self._get_new_img_paths())>=self.rebuild_threshold or not os.path.exists(self.trainer_file)


    def _getImagesAndLabels(self):
        """This reads the the Dataset directory and sets the image path to a label (including both name and id) for the image to be used to train the OpenCV2 model.

        Returns:
            [np.arary]: Numpy array of face images
            [int]: id of the OpenCV face values
            {int:String}: Dictinary of id to a name
        """
        imagePaths = self._get_dataset_img_paths()     
        faceSamples=[]
        name_to_id = {}
        ids= []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L') # grayscale
            img_numpy = np.array(PIL_img,'uint8')
            name = os.path.basename(os.path.dirname(imagePath))
            face_id = int(int.from_bytes(name.encode("utf-8"),"little") % 256)
            name_to_id[name]=face_id
            ids.append(face_id)
            faceSamples.append(img_numpy[:,:])
        return faceSamples,ids,{v:k for k,v in name_to_id.items()}

            
    def build_yml(self):
        """Trains a model and exports it to a yml file and saves the name to id lookup to a json file

        Returns:
            String: Path like String to the trainer.yml in the local file system.
            String: Path like to the mapping json file.

        """
        faceSamples,ids,names = self._getImagesAndLabels()
        with open(self.names_file,'w') as f:
            json.dump(names,f,indent='\t')
            
        recognizer= cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(faceSamples, np.array(ids))
        recognizer.write(self.trainer_file) 
        return self.trainer_file, self.names_file







if __name__=="__main__":
    main(*sys.argv[1:])

