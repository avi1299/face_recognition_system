from flask import Flask, render_template, url_for, request, redirect, flash
from register import register_yourself
from mark_attendance import mark_your_attendance
from deregister import deregister_yourself


app = Flask(__name__)
app.secret_key = 'my secret key'      #Nothing important, type anything, just for flashing
location="LIBRARY"

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/HAR', methods=['GET', 'POST'])
def home_after_registration():
    id = request.form['Student_id']
    register_yourself(id)
    flash("Registration Successful")
    return render_template("index.html")


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    return render_template("register.html")

@app.route('/HAD', methods=['GET', 'POST'])
def home_after_deregistration():
    id = request.form['Student_id']
    if(deregister_yourself(id)):
        flash("Deregistration Successful")
    else:
        flash("ID not found for Deregistration")
    return render_template("index.html")

@app.route('/deregistration', methods=['GET', 'POST'])
def deregistration():
    return render_template("deregister.html")

@app.route('/registration_page', methods=['GET', 'POST'])
def registration_page():
    return render_template("registration_page.html")

@app.route('/attendance_in', methods=['GET', 'POST'])
def attendance_in():
    marked = mark_your_attendance(location)
    if(marked == True):
        flash("Attendence Marked Successfully")
    else:
        flash("You are not registered yet")

    return render_template("index.html")

# @app.route('/attendance_out', methods=['GET', 'POST'])
# def attendance_out():
#     marked = mark_your_attendance(1)
#     if(marked == True):
#         flash("Attendence Marked Successfully")
#     else:
#         flash("You are not registered yet")

#     return render_template("index.html")


if __name__ == '__main__':
    app.run(debug = True)
