# pylint: disable-all

import face_recognition.api as face_recognition
import os, time, pickle
from cv2 import cv2
import numpy as np
import json
#import matplotlib.pyplot as plt
import matplotlib as mpl
import dlib
from imutils.face_utils import rect_to_bb
from imutils.face_utils import FaceAligner
from modules import imageEnhancement
from modules.config import DATA_PATH,LANDMARK_PATH,STORAGE_PATH

def is_already_reg(student_id):
    #Loading the indices for the number of pictures stored per user
    try:
        with open( os.path.join(STORAGE_PATH, "id_idx.json"),"r") as fp:
            id_idx = json.load(fp)
    except:
        id_idx = {}

    #If the registration corresponding to the given ID already exists, return false
    if(student_id in id_idx.keys()):
        return (True,id_idx)    
    else:
        return (False,id_idx)

def register_yourself(student_id,frame_num,image_num,id_idx):

    try:
        os.makedirs(DATA_PATH)
    except:
        pass
    
    #Loading the stored face encodings and corresponding IDs
    try:
        with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"rb") as fp:
            known_face_ids = pickle.load(fp)
        with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"rb") as fp:
            known_face_encodings = pickle.load(fp)
    except:
        known_face_encodings = []
        known_face_ids = []

    mpl.rcParams['toolbar'] = 'None'
    
    print("[INFO] Loading Face Detector")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(LANDMARK_PATH)  
    fa = FaceAligner(predictor, desiredFaceWidth = 96)

    print("[INFO] Initializing Video stream")
    vs = cv2.VideoCapture(0)#,cv2.CAP_DSHOW)
    
    #Uncommnet below to create the folder for the images
    '''
    IMAGE_PATH = os.path.join(DATA_PATH, student_id)
    try:
        os.makedirs(IMAGE_PATH)
    except:
        pass
    '''
    #Entry time
    tin = time.time()

    #frame = vs.read()
    #fig = plt.figure()
    #plot = plt.subplot(1,1,1)
    #plt.title("Detecting Face")
    #plt.axis('off')
    #im1 = plot.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    while image_num < 10:   # Take 10 images
        
        _,frame = vs.read()
        frame_num += 1

        #Resize each image
        #frame = cv2.resize(frame ,(600,600))
        
        #Applying face enhancement steps
        frame =imageEnhancement.adjust_gamma(frame,gamma = 1.5)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        #Detecting faces in the frame
        faces = detector(gray_frame,0)
        
        for face in faces:

            if face is None:
                print("face is none")
                continue
            
            #Capture the face and align it using the face aligner
            (x,y,w,h) = rect_to_bb(face)
            face_aligned = fa.align(frame,gray_frame,face)
            face_aligned = cv2.resize(face_aligned ,(600,600))
            
            # @params the initial point of the rectangle will be x,y and
            # @params end point will be x+width and y+height
            # @params along with color of the rectangle
            # @params thickness of the rectangle
            #Put a bounding box over detected face
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
            
            #cv2.imshow("Image Captured",frame)
            #cv2.waitKey(50)

        #plt.ion()
        #im1.set_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        #plt.pause(0.001)
        #plt.show()
        
        if(frame_num % 30 == 0):
            
            #Uncommnet the line below to store the face images
            #cv2.imwrite(IMAGE_PATH + "/{}_".format(student_id) + str(j) + ".jpg", face_aligned)

            #Appending the face encodings and corresponding IDs 
            try:
                known_face_encodings.append(face_recognition.face_encodings(frame)[0])
                known_face_ids.append(student_id)
            except:
                continue
            image_num += 1



        #OpenCV's implementation to show an image in window(doesn't work on production server)
        #cv2.imshow("Capturing Images for registration (PRESS Q TO QUIT",frame)
        
        #Encoding the frame to be stream into browser
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


        #if(cv2.waitKey(1) == ord("q")):
        #    break

    #Storing the face encodings and corresponding IDs to disk
    with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"wb") as fp:
        pickle.dump(known_face_ids,fp)
    with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"wb") as fp:
        pickle.dump(known_face_encodings,fp)

    #Noting the number of pictures already captured and storing the index
    id_idx[student_id] = image_num
    with open( os.path.join(STORAGE_PATH, "id_idx.json"),"w") as outfile:
        json.dump(id_idx, outfile)

    #Exit time
    tout = time.time()
    print(tout - tin)

    #plt.close()

    #Releasing the videostream
    vs.release()
    cv2.destroyAllWindows()
    return True

def add_photos(student_id,frame_num,image_num,id_idx,start_idx):

    try:
        os.makedirs(DATA_PATH)
    except:
        pass

    #Loading the stored face encodings and corresponding IDs
    try:
        with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"rb") as fp:
            known_face_ids = pickle.load(fp)
        with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"rb") as fp:
            known_face_encodings = pickle.load(fp)

    except:
        known_face_encodings = []
        known_face_ids = []

    mpl.rcParams['toolbar'] = 'None'
    
    print("[INFO] Loading Face Detector")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(LANDMARK_PATH)  
    fa = FaceAligner(predictor, desiredFaceWidth = 96)

    print("[INFO] Initializing Video stream")
    vs = cv2.VideoCapture(0)#,cv2.CAP_DSHOW)

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
    tin = time.time()

    #i = 0
    #j = start

    while image_num < start_idx + 10:   # Take 10 images

        frame_num += 1
        _,frame = vs.read()

        #Resize each image
        #frame = cv2.resize(frame , (600,600))
        
        #Applying face enhancement steps
        frame =imageEnhancement.adjust_gamma(frame,gamma = 1.5)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Detecting faces in the frame
        faces = detector(gray_frame,0)
        
        for face in faces:

            if face is None:
                print("face is none")
                continue

            #Capture the face and align it using the face aligner
            (x,y,w,h) = rect_to_bb(face)
            face_aligned = fa.align(frame,gray_frame,face)
            face_aligned = cv2.resize(face_aligned ,(600,600))

            # @params the initial point of the rectangle will be x,y and
            # @params end point will be x+width and y+height
            # @params along with color of the rectangle
            # @params thickness of the rectangle
            #Put a bounding box over detected face
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
            
            #cv2.imshow("Image Captured",frame)
            #cv2.waitKey(50)
            if(frame_num % 30 == 0):
            
                #Uncommnet the line below to store the face files
                #cv2.imwrite(IMAGE_PATH + "/{}_".format(student_id) + str(j) + ".jpg", face_aligned)

                #Appending the face encodings and corresponding IDs 
                try:
                    known_face_encodings.append(face_recognition.face_encodings(frame)[0])
                    known_face_ids.append(student_id)
                except:
                    continue
                image_num += 1

        #OpenCV's implementation to show an image in window(doesn't work on production server)
        #cv2.imshow("Capturing Images for registration (PRESS Q TO QUIT",frame)
        
        #Encoding the frame to be stream into browser
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        #if(cv2.waitKey(1) == ord("q")):
        #    break
        
        
    #Storing the face encodings and corresponding IDs to disk
    with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"wb") as fp:
        pickle.dump(known_face_ids,fp)
    with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"wb") as fp:
        pickle.dump(known_face_encodings,fp)

    #Noting the number of pictures already captured and storing the index
    id_idx[student_id] = image_num

    with open( os.path.join(STORAGE_PATH, "id_idx.json"),"w") as outfile:
        json.dump(id_idx, outfile)

    #Exit time
    tout = time.time()
    print(tout - tin)

    #plt.close()

    #Releasing the videostream
    vs.release()
    cv2.destroyAllWindows()
    return True

def deregister_yourself(student_id):
    #print("Inside deregister yourself")
    try:
        os.makedirs(DATA_PATH)
    except:
        pass
    
    #Loading the stored face encodings and corresponding IDs
    try:
        with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"rb") as fp:
            known_face_ids = pickle.load(fp)
        with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"rb") as fp:
            known_face_encodings = pickle.load(fp)

    except:
        known_face_encodings = []
        known_face_ids = []

    #Loading the indices for the number of pictures stored per user
    try:
        with open( os.path.join(STORAGE_PATH, "id_idx.json"),"r") as fp:
            id_idx = json.load(fp)
    except:
        id_idx = {}

    #If there doesn't exists any registration corresponding to the given ID, return false
    if student_id not in id_idx.keys():
        return False

    #Remove the data corresponding to the given ID
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

