import json

from Src.models import *
from Util.database import db
from Util.email import send_email
from appConfig import app
import win32api
from flask import request, render_template

app.config['SECRET_KEY'] = 'qwertyuiop'

x = []

import Src.models
import Src.WebAPIs


@app.route('/')
def index():
    return render_template("homepage.html")


@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        user = db.session.query(DoctorModel).filter_by(email=username).first()

        db.session.commit()
        if user is None:
            return render_template("homepage.html")
        elif password != user.password:
            return render_template("homepage.html")
        else:
            return render_template("doctorregistration.html")
    else:
        return render_template("doctorhomepage.html")


@app.route('/doctor/passwordreset', methods=['GET', 'POST'])
def doctorpaswordreset():
    return render_template("doctorpasswordresetpage.html")


@app.route('/doctor/doctorregistration', methods=['GET', 'POST'])
def doctorregistration():
    if request.method == 'POST':
        y = json.dumps(request.form)
        data = json.loads(y)

        # data = request.get_json()
        new_doctor = DoctorModel(Name=data['name'], DOB=data['dob'], PhoneNumber=data['PhoneNumber'],
                                 specialization=data['specialization'], email=data['email'], password=data['password'])

        db.session.add(new_doctor)
        db.session.commit()

        email_body = "You are successfully registered {} <{}>.".format(new_doctor.Name, new_doctor.email)
        email_html = render_template("doctorresetpassword.html", username=new_doctor.Name,
                                     link="http://127.0.0.1:5000/doctor/passwordreset")
        send_email(new_doctor.email, '', "Confirmation Email", email_body, email_html)
        return render_template("adminhomepage.html")
    else:
        return render_template("doctorregistration.html")


@app.route('/radiologist', methods=['GET', 'POST'])
def radiologist():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        user = db.session.query(RadiologistModel).filter_by(email=username).first()

        db.session.commit()
        if user is None:
            return render_template("homepage.html")
        elif password != user.password:
            return render_template("homepage.html")
        else:
            return render_template("radiologistregistrationpage.html")
    else:
        return render_template("radiologisthomepage.html")


@app.route('/radiologist/radiologistregistration', methods=['GET', 'POST'])
def radiologistregistration():
    if request.method == 'POST':

        re = json.dumps(request.form)
        r = json.loads(re)

        # data = request.get_json()
        new_radiologist = RadiologistModel(Name=r['name'], DOB=r['dob'], PhoneNumber=r['PhoneNumber'],
                                           specialization=r['specialization'], email=r['email'], password=r['password'])
        db.session.add(new_radiologist)
        db.session.commit()
        return render_template("adminhomepage.html")
    else:
        return render_template("radiologistregistrationpage.html")


# @app.route('/admin', methods=['GET', 'POST'])
# def admin():
# return render_template("adminlogin.html")


@app.route('/admin/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    if request.method == 'POST':
        adusername = request.form["username"]
        adpassword = request.form["password"]

        adminuser = db.session.query(AdminModel).filter_by(email=adusername, password=adpassword).first()

        db.session.commit()

        if adminuser is None:
            return render_template("adminregistration.html")
        else:
            win32api.MessageBox(0, adminuser.Name + " LoggedIn", 'Admin Response')
            return render_template("adminhomepage.html")
    else:
        return render_template("adminlogin.html")


@app.route('/admin/adminLogin/adminhomepage', methods=['GET', 'POST'])
def adminhomepage():
    return render_template("adminhomepage.html")


@app.route('/patient/patientregistration', methods=['GET', 'POST'])
def patientregistration():
    if request.method == 'POST':

        pa = json.dumps(request.form)
        p = json.loads(pa)

        # data = request.get_json()
        new_patient = PatientModel(Name=p['name'], DOB=p['dob'], Guardianname=p['guardianname'],
                                   PhoneNumber=p['PhoneNumber'], Address=p['address'], email=p['email'],
                                   password=p['password'])
        db.session.add(new_patient)
        db.session.commit()
        message = "Successfully Registered"
        return render_template("adminhomepage.html")
    else:
        return render_template("patientregistration.html")


@app.route('/patient', methods=['GET', 'POST'])
def patient():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        user = db.session.query(PatientModel).filter_by(email=username).first()

        db.session.commit()
        if user is None:
            return render_template("homepage.html")
        elif password != user.password:
            return render_template("homepage.html")
        else:
            return render_template("radiologistregistrationpage.html")
    else:
        return render_template("patienthomepage.html")


if __name__ == "__main__":
    app.run(debug=True)
