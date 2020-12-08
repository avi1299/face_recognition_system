# Face Recognition Surveillance System

## Project Objective

- To design a real-time face recognition system that identifies people across the **BITS Pilani, Pilani campus**. Live video footage is provided as an input through the **100+** CCTV cameras installed at various vital locations across the campus. 
- To design a **web portal** that can allow registration of users with the option to add more photos. 
- To create the face recognition module which will recognize multiple faces in a given frame and the log should be stored in a database. 


## Instructions to run

Optionally, create a virtual environment on your system and open it. 

To run the application, first clone the repository by typing the command in git bash.
```
git clone https://github.com/avi1299/face_recognition_system.git

```
Alternatively, you can download the code as .zip and extract the files.


Shift to the cloned directory

```
cd face_recognition_system
```

To install the requirements, run the following command:

```
pip install -r requirements.txt
```

Go to modules/config.py and set your `PROJECT_PATH`

To launch the application, run the following command: 

```
python3 __init__.py
```

Go to: `localhost:5000` in your browser.

First Register yourself by clicking on `Registration` and then on `New Registration`.

Mark your attendance by clicking on `Mark Attendance` button on the home page.

Additionally one can `Add photos` or `Delete Registration` from the Registration page.

The system offers an use-case of analyzing stored footages. To analyze a footage, it should be stored in the `storage/footage` directory. Next go to the `footage analysis` section and enter the full name (with extension) of the clip. The system will run its algorithm on the footage and store relevant entries into the database. 

You can watch the [demo video here](https://drive.google.com/file/d/1H8JPD-QQFenn6lgoRUsNRNceKmF0tpx2/view?usp=sharing)
## Algorithm

Our algorithm is divided into three main parts:
1. Face Detection
2. Preprocessing
3. Face  recognition
4. Web application development

### Phase 1: Face detection

We have used `Dlib`'s Histogram Oriented Gradients (HOG) based detector that is quick and accurate and hence usable for real time detection of faces. The cropped face from bounding box is passed forward for preprocessing.

![HOG](./static/Images/HOG.PNG?raw=true "HOG")



### Phase 2 : Preprocessing

- The live video input from the CCTV camera is divided into frames at the rate of `30` frames per sec.
- Each frame goes three preprocessing steps.

#### STEP 1: Gamma correction

Gamma correction operation performs nonlinear brightness adjustment. Brightness for darker pixels is increased, but it is almost the same for bright pixels. As a result more details are visible.

#### STEP 2: Wiener filtering

A wiener filter is applied to remove the blur in an image caused by linear motion or unfocused optics. Wiener filters are far and away the most common deblurring technique used because it mathematically returns the best results.

#### STEP 3: Alignment

Sixty-eight landmark points are identified on the face using the `Dlib` python library. 

![Dlib_Landmark_Points](./static/Images/Dlib_Landmark_Points.PNG?raw=true "Dlib_Landmark_Points")

- The above recognized facial landmark points are used for alignment purposes. We perform *affine transformation* using the above-recognised landmark points. Facial recognition algorithms perform better on aligned faces.

###  PHASE 3 : Face recognition

- Our model proposes a solution that uses **10 images per user** to detect the identity. 
- **128-dimensional embeddings** are generated for each of the faces using the `face_recognition` library. The embeddings are stored and matched when face recognition model is called.

### PHASE 4 - Web Application Development

We built a web platform where students can register themselves and mark their attendance once registered.

![Home_Page](./static/Images/Home_Page.PNG?raw=true "Home_Page")

![Registration_Page](./static/Images/Registration_Page.PNG?raw=true "Registration_Page")

![Identity_Recognition](./static/Images/Identity_Recognition.PNG?raw=true "Identity_Recognition")

## Error Analysis

The possible reasons for the errors could be: 
1. Change in the person’s face over time - considerable facial change from the photo used in training. 
2. Two or more similar looking people - If there are multiple people with similar faces, then the model may wrongly classify a person as someone else. 
3. Lack of training data - Deep learning networks are known to increase their accuracy in increasing the data. Since we have only one image per person, therefore there is scope for the model to be trained more efficiently.


## Contributors

1. Avinash Sontakke [Profile](https://github.com/avi1299)
2. Shrey Shah [Profile](https://github.com/imshreyshah)
3. Vishal Mittal [Profile](https://github.com/vismit2000)
4. Harsh Sulakhe [Profile](https://github.com/HarshSulakhe)
