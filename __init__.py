# pylint: disable-all

from flask import Flask, render_template, url_for, request, redirect, flash, Response
from face_recognition_system.modules.register import register_yourself, deregister_yourself, add_photos
from face_recognition_system.modules.mark_attendance import mark_your_attendance
from face_recognition_system.modules.footageAnalysis import analyseFootage

app = Flask(__name__)
app.secret_key = 'my secret key'      #Nothing important, type anything, just for flashing
location="LIBRARY"

@app.route('/')
def render_homepage():
    return render_template("index.html")


@app.route('/HAR', methods=['GET', 'POST'])
def home_after_registration():
    id = request.form['Student_id']
    if(register_yourself(id)):
        flash("Registration Successful")
    else:
        flash("Registration already Exists. Either delete registration or add photos")
    return render_template("index.html")

@app.route('/HAD', methods=['GET', 'POST'])
def home_after_deregistration():
    id = request.form['Student_id']
    if(deregister_yourself(id)):
        flash("Deregistration Successful")
    else:
        flash("ID not found for Deregistration")
    return render_template("index.html")


@app.route('/HAA', methods=['GET', 'POST'])
def home_after_addphotos():
    id = request.form['Student_id']
    if(add_photos(id)):
        flash("Photos added Successful")
    else:
        flash("Registration doesn't exist. Please Register yourself first")
    return render_template("index.html")


@app.route('/registration', methods=['GET', 'POST'])
def render_registration():
    return render_template("register.html")

@app.route('/deregistration', methods=['GET', 'POST'])
def render_deregistration():
    return render_template("deregister.html")

@app.route('/addphotosfn', methods=['GET', 'POST'])
def render_addphotosfn():
    return render_template("addphotos.html")

@app.route('/registration_page', methods=['GET', 'POST'])
def render_registration_page():
    return render_template("registration_page.html")

@app.route('/attendance_in', methods=['GET', 'POST'])
def attendance_in():
    marked = mark_your_attendance(location)
    if(marked == True):
        flash("Attendence Marked Successfully")
    else:
        flash("You are not registered yet")

    return render_template("index.html")

@app.route('/footage-analysis', methods=['GET', 'POST'])
def render_footage_analysis():
    return render_template("footageanalysis.html")

@app.route('/HAFA', methods=['GET', 'POST'])
def home_after_analysis():
    clipname = request.form['Clip_name']
    if(analyseFootage(clipname)):
        flash("Analysis done and entries are stored in the database")
    else:
        flash("File does not exist. Check name again")   

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug = True)
