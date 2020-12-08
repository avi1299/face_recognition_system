# pylint: disable-all

import pickle, os
import face_recognition.api as face_recognition
from cv2 import cv2
import numpy as np
import matplotlib as mpl
#import sqlite3
import psycopg2
from modules.config import STORAGE_PATH, DB_PATH
from modules import imageEnhancement

def no_regs_yet():
    try:
        with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"rb") as fp:
            known_face_ids = pickle.load(fp)
        with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"rb") as fp:
            known_face_encodings = pickle.load(fp)
    except:
        known_face_encodings = []
        known_face_ids = []

    if known_face_ids==[]:
        return (True,known_face_encodings,known_face_ids)
    else :
        return (False,known_face_encodings,known_face_ids)

def mark_your_attendance(location,known_face_encodings,known_face_ids):

    mpl.rcParams['toolbar'] = 'None'

    
    if(os.path.exists(DB_PATH)):
        #rdbms='sqlite'
        #conn = psycopg2.connect(DB_PATH)
        #c=conn.cursor()
        rdbms='postgresql'
        conn = psycopg2.connect(host="localhost",database="face_rec_db",user="postgres",password="atmanirbhar")
        c=conn.cursor()
    else:
        #os.mknod(DB_PATH)
        conn = sqlite3.connect(DB_PATH)
        c=conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS ATTENDANCE
         (ID        TEXT   NOT NULL,
         TIMESTAMP  TEXT       NOT NULL,
         LOCATION  TEXT);''')
        conn.commit()

    name = "Unknown"
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    sanity_count = 0
    unknown_count = 0
    marked = True

    video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    #_,frame = video_capture.read()

    while True:
        # Grab a single frame of video
        _,frame = video_capture.read()

        #Applying face enhancement steps
        frame =imageEnhancement.adjust_gamma(frame,gamma = 1.5)

        # Resize frame of video to 1/4 size for faster face recognition processing
        #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        small_frame = frame
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

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
                except:
                    # print("No students have been marked")
                    video_capture.release()
                    cv2.destroyAllWindows()
                    marked = False
                    return marked
                if matches[best_match_index]:
                    name = known_face_ids[best_match_index]

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


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            #top *= 4
            #right *= 4
            #bottom *= 4
            #left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)

        # print("AFTER SHOWING")
        # Hit 'q' on the keyboard to quit!
        if(sanity_count == 0):
            prev_name = name
            sanity_count += 1

        elif sanity_count < 60 :
            if(prev_name == name and name != "Unknown"):
                sanity_count += 1
                prev_name = name
            else:
                sanity_count = 0

        elif sanity_count == 60 :
            # print("Face registered")
            # video_capture.release()
            # cv2.destroyAllWindows()
            sanity_count = 0
            # now = datetime.now()
            # if(entry_or_exit==0):
            #     c.execute("INSERT INTO ATTENDANCE VALUES (?,datetime('now'),'IN');",(name, ))
            # else:
            #     c.execute("INSERT INTO ATTENDANCE VALUES (?,datetime('now'),'OUT');",(name, ))
            
            if (rdbms=='sqlite'):
                c.execute("INSERT INTO ATTENDANCE VALUES (?,datetime('now'),?);",(name, location, ))
            elif (rdbms=='postgresql'):
                c.execute("INSERT INTO attendance VALUES (%s,now(),%s);",(name, location))
            conn.commit()
            
            break

        #OpenCV's implementation to show an image in window(doesn't work on production server)
        #cv2.imshow("Marking Attendance (PRESS Q TO QUIT)",frame)
        
        #Encoding the frame to be stream into browser
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        #if cv2.waitKey(20) == ord("q"):
        #    break


    # Release handle to the webcam

    #plt.close()
    video_capture.release()
    cv2.destroyAllWindows()
    conn.close()

    return marked

# mark_your_attendance()
