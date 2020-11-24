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
from modules.config import DATA_PATH,PROJECT_PATH,LANDMARK_PATH,STORAGE_PATH

def register_yourself(student_id):

    try:
        os.makedirs(DATA_PATH)
    except:
        pass

    try:
        with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"rb") as fp:
            known_face_ids = pickle.load(fp)
        with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"rb") as fp:
            known_face_encodings = pickle.load(fp)
    except:
        known_face_encodings = []
        known_face_ids = []

    try:
        with open( os.path.join(STORAGE_PATH, "id_idx.json"),"r") as fp:
            id_idx = json.load(fp)
    except:
        id_idx = {}

    if(student_id in id_idx.keys()):
        return False

    mpl.rcParams['toolbar'] = 'None'
    
    print("[INFO] Loading Face Detector")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(LANDMARK_PATH)  
    fa = FaceAligner(predictor, desiredFaceWidth = 96)

    print("[INFO] Initializing Video stream")
    vs = VideoStream(src=0).start()
    
    #Below is the OpenCV implementation for capturing from webcam
    #video_capture = cv2.VideoCapture(0)
    
    #Uncommnet below to create the foler for the images
    '''
    IMAGE_PATH = os.path.join(DATA_PATH, student_id)
    try:
        os.makedirs(IMAGE_PATH)
    except:
        pass
    '''

    #Entry time
    tic = time.time()

    i = 0
    j = 0

    frame = vs.read()
    fig = plt.figure()
    plot = plt.subplot(1,1,1)
    plt.title("Detecting Face")
    plt.axis('off')
    im1 = plot.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

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
            
            #cv2.imshow("Image Captured",frame)
            # Before continuing to the next loop, I want to give it a little pause
            # waitKey of 50 millisecond
            #cv2.waitKey(50)

        plt.ion()
        im1.set_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.pause(0.001)
        plt.show()
        if(i % 30 == 0):
            
            # Uncommnet the line below to store the face images
            #cv2.imwrite(IMAGE_PATH + "/{}_".format(student_id) + str(j) + ".jpg", face_aligned)

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

    id_idx[student_id] = 10

    with open( os.path.join(STORAGE_PATH, "id_idx.json"),"w") as outfile:
        json.dump(id_idx, outfile)

    #Exit time
    toc = time.time()
    print(toc - tic)

    plt.close()
    vs.stop()
    cv2.destroyAllWindows()
    return True

def add_photos(student_id):

    try:
        os.makedirs(DATA_PATH)
    except:
        pass

    try:
        with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"rb") as fp:
            known_face_ids = pickle.load(fp)
        with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"rb") as fp:
            known_face_encodings = pickle.load(fp)

    except:
        known_face_encodings = []
        known_face_ids = []

    try:
        with open( os.path.join(STORAGE_PATH, "id_idx.json"),"r") as fp:
            id_idx = json.load(fp)
    except:
        id_idx = {}

    if(student_id not in id_idx.keys()):
        return False

    mpl.rcParams['toolbar'] = 'None'
    
    print("[INFO] Loading Face Detector")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(LANDMARK_PATH)  
    fa = FaceAligner(predictor, desiredFaceWidth = 96)

    print("[INFO] Initializing Video stream")
    vs = VideoStream(src=0).start()

    #OpenCV implementation 
    #video_capture = cv2.VideoCapture(0)

    #Uncommnet below to create the foler for the images
    '''
    IMAGE_PATH = os.path.join(DATA_PATH, student_id)
    try:
        os.makedirs(IMAGE_PATH)
    except:
        pass
    '''
    try:
        start = id_idx[student_id]
    except :
        start = 0

    #Entry time
    tic = time.time()

    i = 0
    j = start

    frame = vs.read()
    plot = plt.subplot(1,1,1)
    plt.title("Detecting Face")
    plt.axis('off')
    im1 = plot.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    while j < start + 10:   # Take 10 images

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
            
            #cv2.imshow("Image Captured",frame)
            # Before continuing to the next loop, I want to give it a little pause
            # waitKey of 50 millisecond
            #cv2.waitKey(50)

        plt.ion()
        im1.set_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.pause(0.001)
        plt.show()
        if(i % 30 == 0):
            
            # Uncommnet the line below to store the face files

            #cv2.imwrite(IMAGE_PATH + "/{}_".format(student_id) + str(j) + ".jpg", face_aligned)

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

    with open( os.path.join(STORAGE_PATH, "id_idx.json"),"w") as outfile:
        json.dump(id_idx, outfile)

    #Exit time
    toc = time.time()
    print(toc - tic)

    plt.close()
    vs.stop()
    cv2.destroyAllWindows()
    return True

def deregister_yourself(student_id):
    #print("Inside deregister yourself")
    try:
        os.makedirs(DATA_PATH)
    except:
        pass

    try:
        with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"rb") as fp:
            known_face_ids = pickle.load(fp)
        with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"rb") as fp:
            known_face_encodings = pickle.load(fp)

    except:
        known_face_encodings = []
        known_face_ids = []

    try:
        with open( os.path.join(STORAGE_PATH, "id_idx.json"),"r") as fp:
            id_idx = json.load(fp)
    except:
        id_idx = {}

    if student_id not in id_idx.keys():
        return False

    new_face_id=[]
    new_face_encoding=[]
    for index,val in enumerate(known_face_ids):
        if(val!=student_id):
            new_face_id.append(known_face_ids[index])
            new_face_encoding.append(known_face_encodings[index])
    known_face_ids=new_face_id
    known_face_encodings=new_face_encoding
    #print(known_face_ids)

    with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"wb") as fp:
        pickle.dump(known_face_ids,fp)
    with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"wb") as fp:
        pickle.dump(known_face_encodings,fp)

    id_idx.pop(student_id)

    with open( os.path.join(STORAGE_PATH, "id_idx.json"),"w") as outfile:
        json.dump(id_idx, outfile)
    
    return True

