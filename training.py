import cv2
import numpy as np
from PIL import Image
import os
import sys
import glob
import hashlib
import json

def main(*paths, traner_file ='trainer.yml', classifier="D:\Python\Lib\site-packages\cv2\data\haarcascade_frontalface_alt.xml", **kargs):
    # Path for face image database
    detector = cv2.CascadeClassifier(classifier)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    

    # function to get the images and label data
    def getImagesAndLabels(paths):
        imagePaths = [p for g in paths for p in glob.glob(g)]     
        faceSamples=[]
        ids = []
        names = {}
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L') # grayscale
            img_numpy = np.array(PIL_img,'uint8')
            name = os.path.basename(os.path.dirname(imagePath))
            face_id = int(hashlib.md5(name.encode('utf-8')).hexdigest()[-5:], 16)
            names[face_id]=name
            faces = detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(face_id)
        return faceSamples,ids,names
    
    print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        
    faces,ids,names = getImagesAndLabels(paths)
    json.dump(names,open("names.json",'w'),indent='\t')
    recognizer.train(faces, np.array(ids))

    # Save the model into trainer/trainer.yml
    recognizer.write(traner_file) 
    # Print the numer of faces trained and end program
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))

if __name__=="__main__":
    main(*sys.argv[1:])