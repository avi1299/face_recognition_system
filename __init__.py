# pylint: disable-all

from flask import Flask, render_template, url_for, request, redirect, flash, Response
from modules.register import register_yourself, deregister_yourself, add_photos, is_already_reg
from modules.mark_attendance import mark_your_attendance, no_regs_yet
from modules.footageAnalysis import analyseFootage
import psycopg2

app = Flask(__name__)
app.secret_key = 'my secret key'      #Nothing important, type anything, just for flashing
location="LIBRARY"

@app.route('/',methods=['GET', 'POST'])
def render_homepage():
    return render_template("index.html")

@app.route('/registration_page', methods=['GET', 'POST'])
def render_registration_page():
    return render_template("registration_page.html")

####### FUNCTIONALITY TO REGISTER YOURSELF ########
@app.route('/registration', methods=['GET', 'POST'])
def render_registration():
    return render_template("register.html")

@app.route('/registration/reg-vid-feed', methods=['GET', 'POST'])
def home_after_registration():
    global stud_id 
    stud_id = request.form['Student_id']
    name=request.form['Student_Name']
    name=name.lower()
    conn = psycopg2.connect(host="localhost",database="face_rec_db",user="postgres",password="atmanirbhar")
    c=conn.cursor()
    c.execute("SELECT count(*) FROM identity WHERE name = %(name)s and id_no=%(id_no)s;", {'name': name,'id_no':stud_id})
    res,=c.fetchone()
    conn.close()
    if(res!=1):
        flash("Name and ID not consistent with AUGSD database")
        return render_template("index.html")
    global id_idx
    reg,id_idx = is_already_reg(stud_id)
    if reg:
        flash("Registration already Exists. Either delete registration or add photos")
        return render_template("registration_page.html")
    #elif(register_yourself(id)):
    #    flash("Registration Successful")
    #else:
    #    flash("Registration already Exists. Either delete registration or add photos")
    return render_template("reg-vid-feed.html")

@app.route('/reg_vid_feed')
def reg_vid_feed():
    frame_num = 0
    image_num = 0
    return Response(register_yourself(stud_id,frame_num,image_num,id_idx), mimetype='multipart/x-mixed-replace; boundary=frame')

###############################################################################

##### FUNCTIONALITY TO ADD MORE PHOTOS TO YOUR REGISTRATION #############
@app.route('/addphotosfn', methods=['GET', 'POST'])
def render_addphotosfn():
    return render_template("addphotos.html")

@app.route('/addphotosfn/addp-vid-feed', methods=['GET', 'POST'])
def home_after_addphotos():
    global stud_id2 
    stud_id2 = request.form['Student_id']
    #if(add_photos(id)):
    #    flash("Photos added Successful")
    #else:
    #    flash("Registration doesn't exist. Please Register yourself first")
    global id_idx2
    reg,id_idx2 = is_already_reg(stud_id2)
    if not reg:
        flash("Registration doesn't exist. Please Register yourself first")
        return render_template("registration_page.html")

    return render_template("addp-vid-feed.html")

@app.route('/addp_vid_feed')
def addp_vid_feed():
    frame_num = 0
    start_idx = id_idx2[stud_id2]
    image_num = start_idx
    return Response(add_photos(stud_id2,frame_num,image_num,id_idx2,start_idx), mimetype='multipart/x-mixed-replace; boundary=frame')

########################################################################

######### FUNCTIONALITY TO DEREGISTER YOURSELF ################################## 
@app.route('/deregistration', methods=['GET', 'POST'])
def render_deregistration():
    return render_template("deregister.html")

@app.route('/HAD', methods=['GET', 'POST'])
def home_after_deregistration():
    id = request.form['Student_id']
    if(deregister_yourself(id)):
        flash("Deregistration Successful")
    else:
        flash("ID not found for Deregistration")
    return render_template("index.html")

############################################################################

############# FUNCTIONALITY TO MARK YOUR ATTENDANCE ######################

@app.route('/attendance_in', methods=['GET', 'POST'])
def attendance_in():
    global known_face_encodings, known_face_ids
    regs,known_face_encodings,known_face_ids = no_regs_yet()
    #marked = mark_your_attendance(location)
    #if(marked == True):
    #    flash("Attendence Marked Successfully")
    #else:
    #    flash("You are not registered yet")
    if regs == True:
        flash("No Registrations yet!")
        return render_template("index.html")
    else:
        return render_template("mark-att-vid-feed.html")

@app.route('/mark_att_vid_feed')
def mark_att_vid_feed():
    return Response(mark_your_attendance(location,known_face_encodings,known_face_ids), mimetype='multipart/x-mixed-replace; boundary=frame')

############################################################################

#################### FUNCTIONALITY TO ANALYzE CCTC FOOTAGES ###################

@app.route('/footage-analysis', methods=['GET', 'POST'])
def render_footage_analysis():
    return render_template("footageanalysis.html")

@app.route('/footage-analysis/footage-feed', methods=['GET', 'POST'])
def home_after_analysis():
    global clipname 
    clipname= request.form['Clip_name']
    #if(analyseFootage(clipname)):
    #    flash("Analysis done and entries are stored in the database")
    #else:
    #    flash("File does not exist. Check name again")   

    return render_template("footagefeed.html")

@app.route('/footage_feed')
def footage_feed():
    return Response(analyseFootage(clipname), mimetype='multipart/x-mixed-replace; boundary=frame')

####################################################################################

if __name__ == '__main__':
    app.run(debug = True)
