from imutils.video import FileVideoStream
#from imutils.video import FPS
import imutils
from threading import Thread
import sys, time, os
from queue import Queue
import dlib
import cv2
from imutils.face_utils import rect_to_bb , FaceAligner
from modules.imageEnhancement import adjust_gamma
from modules.config import FOOTAGES_PATH, LANDMARK_PATH, DB_PATH

def analyseFootage(clipname):
    CLIP_PATH = FOOTAGES_PATH + "/" + clipname

    if(os.path.isfile(CLIP_PATH) == False):
        return 0

    fvs = FileVideoStream(CLIP_PATH).start()
    time.sleep(1.0)

    print("[INFO] Loading the facial detector")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(LANDMARK_PATH)  
    fa = FaceAligner(predictor, desiredFaceWidth = 96)
    
    print("[INFO] Initializing CCTV Footage")
    while fvs.more():
    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale (while still retaining 3
    # channels)
        frame = fvs.read()
        
        if(frame is None):
            break
        
        #frame = imutils.resize(frame ,width = 1000)

        frame =adjust_gamma(frame,gamma = 1.7)
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
        
            x = face.left()
            y = face.top()
            w = face.right() - x
            h = face.bottom() - y
            
            face_aligned = fa.align(frame,gray_frame,face)
            # Whenever the program captures the face, we will write that is a folder
            # Before capturing the face, we need to tell the script whose face it is
            # For that we will need an identifier, here we call it id
            # So now we captured a face, we need to write it in a file
            
            # Saving the image dataset, but only the face part, cropping the rest

            if face is None:
                print("face is none")
                continue


            face_aligned = imutils.resize(face_aligned ,width = 600)
            
            #cv2.imshow("Image Captured",face_aligned)
            
            # @params the initial point of the rectangle will be x,y and
            # @params end point will be x+width and y+height
            # @params along with color of the rectangle
            # @params thickness of the rectangle
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
            # Before continuing to the next loop, I want to give it a little pause
            # waitKey of 100 millisecond
            cv2.waitKey(1)

        #Showing the image in another window
        #Creates a window with window name "Face" and with the image img
        cv2.imshow("Video feed",frame)
        
        cv2.waitKey(1)
        
        #frame = imutils.resize(frame, width=450)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #frame = np.dstack([frame, frame, frame])
        # display the size of the queue on the frame
        #cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
            #(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        # show the frame and update the FPS counter
        #cv2.imshow("Frame", frame)
        #cv2.waitKey(1)
        #fps.update()


    # do a bit of cleanup
    cv2.destroyAllWindows()
    fvs.stop()

    return 1