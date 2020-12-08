# pylint: disable-all

import time, os, pickle
from imutils.video import FileVideoStream
#from imutils.video import FPS
import imutils
import dlib
import cv2
import face_recognition.api as face_recognition
import numpy as np
from flask import flash
#from imutils.face_utils import rect_to_bb , FaceAligner
from modules.imageEnhancement import adjust_gamma
from modules.config import FOOTAGES_PATH, STORAGE_PATH

def analyseFootage(clipname):
    CLIP_PATH = FOOTAGES_PATH + "/" + clipname

    if os.path.isfile(CLIP_PATH) == False :
        return 0

    #Load the known face IDs and encodings for facial recognition
    try:
        with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"rb") as fp:
            known_face_ids = pickle.load(fp)
        with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"rb") as fp:
            known_face_encodings = pickle.load(fp)
    except:
        known_face_encodings = []
        known_face_ids = []

    #Start the Video Stream
    fvs = FileVideoStream(CLIP_PATH).start()
    time.sleep(1.0)

    print("[INFO] Loading the facial detector")
    detector = dlib.get_frontal_face_detector()
    #predictor = dlib.shape_predictor(LANDMARK_PATH)
    #fa = FaceAligner(predictor, desiredFaceWidth = 96)  
    name = "Unknown"
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    #sanity_count = 0
    unknown_count = 0
    marked = True

    print("[INFO] Initializing CCTV Footage")
    while fvs.more():
    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale (while still retaining 3
    # channels)
        frame = fvs.read()

        if frame is None :
            break
        
        frame = imutils.resize(frame ,width = 600)

        frame =adjust_gamma(frame,gamma = 1.5)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        #To store the faces
        #This will detect all the images in the current frame, and it will return the coordinates of the faces
        #Takes in image and some other parameter for accurate result
        faces = detector(gray_frame,0)
        #In above 'faces' variable there can be multiple faces so we have to get each and every face and draw a rectangle around it.

        #sampleNum = sampleNum+1
        for face in faces:
            #num_frames = num_frames + 1
            #print("inside for loop")

            if face is None:
                print("face is none")
                continue
    
            #face_aligned = fa.align(frame,gray_frame,face)
            #face_aligned = imutils.resize(face_aligned ,width = 600)

            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance = 0.35)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_ids[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    # print(face_distances)
                    try:
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = known_face_ids[best_match_index]
                    except:
                        # print("No students have been marked")
                        #video_capture.release()
                        #cv2.destroyAllWindows()

                        marked = False
                        #return marked
                    #if matches[best_match_index]:
                    #    name = known_face_ids[best_match_index]

                    face_names.append(name)

            if name == "Unknown" :
                unknown_count += 1
            else:
                unknown_count = 0

            if unknown_count == 600 :
                # video_capture.release()
                # cv2.destroyAllWindows()
                # print("You haven't been registered")
                marked = False
                unknown_count = 0
                break

            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom + 15), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom + 15), font, 0.4, (255, 255, 255), 1)


        #Showing the image in another window
        #Creates a window with window name "Face" and with the image img
        #cv2.imshow("Video feed (PRESS Q TO QUIT",frame)
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        #if cv2.waitKey(1) == ord("q") :
        #    break
        
    print("here")
    # do a bit of cleanup
    cv2.destroyAllWindows()
    #fvs.stop()
    return 