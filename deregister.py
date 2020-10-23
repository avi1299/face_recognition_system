import os, time, pickle
import numpy as np
import json

def deregister_yourself(student_id):
    #print("Inside deregister yourself")
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
    print(known_face_ids)

    with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"wb") as fp:
        pickle.dump(known_face_ids,fp)
    with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"wb") as fp:
        pickle.dump(known_face_encodings,fp)

    id_idx.pop(student_id)

    with open( os.path.join(STORAGE_PATH, "id_idx.json"),"w") as outfile:
        json.dump(id_idx, outfile)
    
    return True


# register_yourself()
