import cv2
import os
import sys
import cam_feed
import uuid



def make_img_path(dataset_dir, face_id, count):
    return os.path.join(dataset_dir, face_id,f"{count}.jpg")

class video_recog():

    def __init__(self,face_id,dataset_dir="./dataset/"):
        self.dataset_dir=dataset_dir
        self.face_id =face_id
        self.count =0
        self.face_detector = cv2.CascadeClassifier(
        'D:\Python\Lib\site-packages\cv2\data\haarcascade_frontalface_alt.xml')


    def init(self, video_capture):
        try:
            os.mkdir(self.dataset_dir)
        except FileExistsError as e:
            pass
        try:
            print(os.path.dirname(make_img_path(self.dataset_dir,self.face_id,0)))
            os.mkdir(os.path.dirname(make_img_path(self.dataset_dir,self.face_id,0)))
        except FileExistsError as e:
            pass

        video_capture.set(3, 640)  # set video width
        video_capture.set(4, 480)  # set video height

        # For each person, enter one numeric face id
        print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    
    def update(self, ret, img):
        #img = cv2.flip(img, -1)  # flip video image vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            self.count +=1
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # Save the captured image into the datasets folder
            cv2.imwrite(make_img_path(self.dataset_dir, self.face_id,self.count),
                        gray[y:y+h, x:x+w])
            cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27 or self.count >= 30:
            cam_feed.running=False
        


    def destroy(self):
        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cv2.destroyAllWindows()


    
    






if __name__ == "__main__":
    v =video_recog(*sys.argv[1:])
    cam_feed.init.append(v.init)
    cam_feed.update.append(v.update)
    cam_feed.destroy.append(v.destroy)
    cam_feed.main_loop()