import json
from pathlib import Path

import win32api
from flask import render_template, request, redirect

from Src.models import *
from Util.database import db, engine
from Util.email import send_email
from appConfig import app

# app.config['SECRET_KEY'] = 'qwertyuiop'

# region run files
import Src.models
import Src.WebAPIs


# endregion

@app.route('/')
def index():
    return render_template("homepage.html")


# region admin
@app.route('/admin/ResetPassword', methods=['GET', 'POST'])
def resetpassword():
    if request.method == 'GET':
        id = request.args['id']
        user_type = request.args['user_type']
        return render_template("password_reset.html", id=id, user_type=user_type)
    else:
        user_id = request.form["user_id"]
        user_type = request.form["user_type"]
        current_password = request.form["current_password"]
        password = request.form["password"]
        cnfpassword = request.form["cnfpassword"]
        if password != cnfpassword:
            win32api.MessageBox(0, 'Your password and confirmation password do not match.', 'Password Reset failed')
            return redirect(request.referrer)

        user = user_type_dict[user_type].query.filter_by(id=user_id, password=current_password).first()
        if user is None:
            win32api.MessageBox(0, 'Incorrect current password.', 'Password Reset failed')
            return redirect(request.referrer)
        else:
            user.password = password
            db.session.commit()
            win32api.MessageBox(0, 'Password reset done successfully', 'Password Reset')
            return redirect('/')


@app.route('/admin/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    if request.method == 'POST':
        adusername = request.form["username"]
        adpassword = request.form["password"]

        adminuser = db.session.query(AdminModel).filter_by(email=adusername, password=adpassword).first()

        db.session.commit()

        if adminuser is None:
            return render_template("admin_registration.html")
        else:

            # win32api.MessageBox(0, adminuser.name + " LoggedIn", 'Admin Response')
            return render_template("admin_homepage.html")
    else:
        return render_template("admin_login.html")


@app.route('/admin/adminLogin/adminhomepage', methods=['GET', 'POST'])
def adminhomepage():
    return render_template("admin_homepage.html")


# endregion

# region doctor
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
            return render_template("doctor_registration.html")
    else:
        return render_template("doctorhomepage.html")


@app.route('/doctor/doctorregistration', methods=['GET', 'POST'])
def doctorregistration():
    if request.method == 'POST':
        # y = json.dumps(request.form)
        # data = json.loads(y)
        data = request.form
        new_doctor = DoctorModel(name=data['name'], DOB=data['dob'], phone_number=data['phone_number'],
                                 specialization=data['specialization'], email=data['email'], password=data['password'])
        db.session.add(new_doctor)
        db.session.commit()

        # win32api.MessageBox(0, str(new_doctor.id) + " LoggedIn", 'Admin Response')
        link = f"{app.config['AppUrl']}admin/ResetPassword?id={new_doctor.id}&user_type=doctor"

        email_body = "You are successfully registered {} <{}>.".format(new_doctor.name, new_doctor.email)
        email_html = render_template('EmailTemplates/welcome_email.html', username=new_doctor.name, link=link)
        send_email(new_doctor.email, '', "Confirmation Email", email_body, email_html)
        return render_template("admin_homepage.html")
    else:
        return render_template("doctor_registration.html")


@app.route('/api/GetDoctorDetails/<email>/<password>', methods=['GET', 'POST'])
def GetDoctorDetails(email, password):
    # return "My emil is " +email+ " and password is "+ password
    # return "Hello"
    # json = request.get_json()
    value = db.session.query(DoctorModel).filter_by(email=email, password=password).first()
    # win32api.MessageBox(0,    # win32api.MessageBox(0,
    # value.Name+value.email+str(value.DOB)+str(value.id)+value.PhoneNumber+value.specialization+value.password
    # + " LoggedIn", 'Admin Response')
    # value.Name+value.email+str(value.DOB)+str(value.id)+value.PhoneNumber+value.specialization+value.password
    # + " LoggedIn", 'Admin Response')

    db.session.commit()

    if value is None:
        r = {"id": 0}
        res = {"result": r}
        result = json.dumps(res)
        # win32api.MessageBox(0,"invalid",'Admin response')
        return result
    else:
        v = {"id": int(value.id), "name": value.Name, "dob": str(value.DOB), "phonenumber": value.PhoneNumber,
             "specialization": value.specialization, "email": value.email, "password": value.password}
        res = {"result": v}
        # win32api.MessageBox(0,str(v),'Admin Response')

        result = json.dumps(res)
        # result=Response(js, status=200, mimetype=)
        # win32api.MessageBox(0, value.Name + " LoggedIn", 'Admin Response')
        return result


# endregion

# region radiologist
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
            return render_template("radiologist_patient.html")
    else:
        return render_template("radiologisthomepage.html")


@app.route('/radiologist/radiologistregistration', methods=['GET', 'POST'])
def radiologistregistration():
    if request.method == 'POST':

        re = json.dumps(request.form)
        r = json.loads(re)

        # data = request.get_json()
        new_radiologist = RadiologistModel(name=r['name'], DOB=r['dob'], phone_number=r['PhoneNumber'],
                                           specialization=r['specialization'], email=r['email'], password=r['password'])
        db.session.add(new_radiologist)
        db.session.commit()
        return render_template("admin_homepage.html")
    else:
        return render_template("radiologistregistrationpage.html")

@app.route('/radiologist/radiologist_patient', methods=['GET', 'POST'])
def radiologist_patient():
    if request.method == 'POST':
        username = request.form["email"]
        global patient_email
        patient_email = db.session.query(PatientModel).filter_by(email=username).first()

        if patient_email is None:
            return render_template("radiologist_pateint.html")
        else:
            patient_id=patient_email.id
            win32api.MessageBox(0, str(patient_id) + "is the patient id", 'Admin Response')
            return render_template("radiologist_upload.html")
    else:
        return render_template("radiologist_patient.html")

@app.route('/radiologist/radiologist_upload', methods=['GET', 'POST'])
def radiologist_upload():
    return render_template("radiologist_upload.html")

@app.route('/radiologist/radiologist_patient/radiologist_upload/radiologist_comment', methods=['GET', 'POST'])
def radiologist_comment():
    return render_template("radilogistcomments.html")

# endregion

# region patient
@app.route('/patient/patientregistration', methods=['GET', 'POST'])
def patientregistration():
    if request.method == 'POST':

        pa = json.dumps(request.form)
        p = json.loads(pa)

        # data = request.get_json()
        new_patient = PatientModel(name=p['name'], DOB=p['dob'], guardian_name=['guardianname'],
                                   phone_number=p['PhoneNumber'], address=p['address'], email=p['email'],
                                   password=p['password'])
        db.session.add(new_patient)
        db.session.commit()
        message = "Successfully Registered"
        return render_template("admin_homepage.html")
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
            return render_template("radiologist_registration.html")
    else:
        return render_template("patienthomepage.html")


# endregion


if __name__ == "__main__":
    app.run(debug=True, threaded=False)
