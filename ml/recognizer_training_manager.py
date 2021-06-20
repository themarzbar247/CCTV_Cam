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
    initial, ext = os.path.basename(img_path).split(os.extsep,1)
    while os.path.exists(img_path):
        fn = os.path.basename(img_path)
        new_name = "".join([random.choice(CHARSET) for _ in range(10)])
        img_path=img_path.replace(fn, f"{initial}({new_name}){os.extsep}{ext}")
    return img_path

def main(new_find_dir, data_set_dir, rebuild_threshold=10):
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
    def __init__(self, new_find_dir, data_set_dir, rebuild_threshold=10):
        self.rebuild_threshold=rebuild_threshold
        self.new_find_dir = new_find_dir
        self.data_set_dir = data_set_dir
        self.trainer_file = os.path.join(data_set_dir,"trainer.yml")
        self.names_file = os.path.join(data_set_dir,"names.json")

    def _get_new_img_paths(self):
        return glob.glob(os.path.join(self.new_find_dir,"**\\*.jpg"))

    def _get_dataset_img_paths(self):
        return glob.glob(os.path.join(self.data_set_dir,"**\\*.jpg"))

    def copy_dataset_additions(self):
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
        return len(self._get_new_img_paths())>=self.rebuild_threshold or not os.path.exists(self.trainer_file)


    def _getImagesAndLabels(self):
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
        
        faceSamples,ids,names = self._getImagesAndLabels()
        with open(self.names_file,'w') as f:
            json.dump(names,f,indent='\t')
            
        recognizer= cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(faceSamples, np.array(ids))
        recognizer.write(self.trainer_file) 
        return self.trainer_file, self.names_file







if __name__=="__main__":
    main(*sys.argv[1:])

