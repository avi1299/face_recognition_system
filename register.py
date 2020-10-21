import face_recognition.api as face_recognition
import os, time, pickle
from cv2 import cv2
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib as mpl
from modules import imageEnhancement
import dlib
import imutils
from imutils import face_utils
from imutils.video import VideoStream
from imutils.face_utils import rect_to_bb
from imutils.face_utils import FaceAligner

def register_yourself(student_id):

    mpl.rcParams['toolbar'] = 'None'
    # PATH = "/home/harsh/Backup/face-recognition/data"
    #PROJECT_PATH = "D:/Acads/Projects/Identity Detection/face_recognition_system"
    PROJECT_PATH = "/home/avinash/Desktop/Projects/face-recognition-attendance-system"
    PATH = PROJECT_PATH+"/static/data"
    STORAGE_PATH = PROJECT_PATH+"/storage"

    try:
        os.makedirs(PATH)
    except:
        pass

    try:
        with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"rb") as fp:
            known_face_ids = pickle.load(fp)
        with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"rb") as fp:
            known_face_encodings = pickle.load(fp)
        # known_face_ids = np.load("known_face_ids.npy")
        # known_face_encodings = np.load("known_face_encodings.npy")
    except:
        known_face_encodings = []
        known_face_ids = []

    try:
        with open( os.path.join(STORAGE_PATH, "id_idx.json"),"r") as fp:
            id_idx = json.load(fp)
    except:
        id_idx = {}

    LANDMARK_PATH = PROJECT_PATH+"/storage/shape_predictor_68_face_landmarks.dat"
    
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(LANDMARK_PATH)  
    fa = FaceAligner(predictor, desiredFaceWidth = 96)

    print("[INFO] Initializing Video stream")
    vs = VideoStream(0).start()
    #video_capture = cv2.VideoCapture(0)
    # student_id = input("Enter your id: ")

    IMAGE_PATH = os.path.join(PATH, student_id)

    try:
        os.makedirs(IMAGE_PATH)
    except:
        pass

    try:
        start = id_idx[student_id]
    except :
        start = 0

    #Entry time
    tic = time.time()

    i = 0
    j = 0

    while j < 10:   # Take 10 images

        i += 1
        frame = vs.read()

        #Resize each image
        frame = imutils.resize(frame ,width = 600)
        
        #Applying face enhancement steps
        frame =imageEnhancement.adjust_gamma(frame,gamma = 2.0)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        #To store the faces
        #This will detect all the images in the current frame, and it will return the coordinates of the faces
        #Takes in image and some other parameter for accurate result
        faces = detector(gray_frame,0)
        
        for face in faces:
            print("inside for loop")
            
            (x,y,w,h) = face_utils.rect_to_bb(face)


            face_aligned = fa.align(frame,gray_frame,face)
            # Whenever the program captures the face, we will write that is a folder
            # Before capturing the face, we need to tell the script whose face it is
            # For that we will need an identifier, here we call it id
            
            # Saving the image dataset, but only the face part, cropping the rest

            if face is None:
                print("face is none")
                continue

            face_aligned = imutils.resize(face_aligned ,width = 600)

            # @params the initial point of the rectangle will be x,y and
            # @params end point will be x+width and y+height
            # @params along with color of the rectangle
            # @params thickness of the rectangle
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
            
            cv2.imshow("Image Captured",frame)
            # Before continuing to the next loop, I want to give it a little pause
            # waitKey of 50 millisecond
            cv2.waitKey(50)


        plt.show()
        if(i % 30 == 0):
            
            # So now we captured a face, we need to write it in a file
            cv2.imwrite(IMAGE_PATH + "/{}_".format(student_id) + str(j) + ".jpg", face_aligned)
            try:
                known_face_encodings.append(face_recognition.face_encodings(frame)[0])
                known_face_ids.append(student_id)
            except:
                continue
            j += 1

    with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"wb") as fp:
        pickle.dump(known_face_ids,fp)
    with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"wb") as fp:
        pickle.dump(known_face_encodings,fp)

    id_idx[student_id] = start + 10

    vs.stop()
    cv2.destroyAllWindows()

    with open( os.path.join(STORAGE_PATH, "id_idx.json"),"w") as outfile:
        json.dump(id_idx, outfile)

    #Exit time
    toc = time.time()
    print(toc - tic)
    plt.close()
# register_yourself()
