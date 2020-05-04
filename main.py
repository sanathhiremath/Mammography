import json
import pathlib
import string
from pathlib import Path
import random

import requests
import win32api
from flask import render_template, request, redirect

from werkzeug.utils import secure_filename

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
            win32api.MessageBox(0, f'Invalid email or password.', 'Error')
            return redirect(request.referrer)
        else:
            return redirect('/admin/AdminHomepage')
    else:
        return render_template("admin_login.html")


@app.route('/admin/AdminHomepage', methods=['GET', 'POST'])
def adminhomepage():
    return render_template("admin_homepage.html")


# endregion

# region doctor
@app.route('/doctor/DoctorLogin', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = db.session.query(DoctorModel).filter_by(email=username, password=password).first()
        db.session.commit()
        if user is None:
            win32api.MessageBox(0, f'Invalid email or password.', 'Login Error')
            return redirect(request.referrer)
        else:
            return redirect(f'/doctor/doctor_patient?id={user.id}')
    else:
        return render_template("doctor_login.html")


@app.route('/doctor/doctorregistration', methods=['GET', 'POST'])
def doctorregistration():
    if request.method == 'POST':
        data = request.form
        user = db.session.query(DoctorModel).filter_by(email=data['email']).first()
        db.session.commit()
        if user is None:
            new_doctor = DoctorModel(name=data['name'], DOB=data['dob'], phone_number=data['phone_number'],
                                     specialization=data['specialization'], email=data['email'],
                                     password=data['password'])
            db.session.add(new_doctor)
            db.session.commit()
            link = f"{app.config['AppUrl']}admin/ResetPassword?id={new_doctor.id}&user_type=doctor"
            email_body = "You are successfully registered {} <{}>.".format(new_doctor.name, new_doctor.email)
            email_html = render_template('EmailTemplates/welcome_email.html', username=new_doctor.name, link=link)
            send_email(new_doctor.email, '', "Confirmation Email", email_body, email_html)
            win32api.MessageBox(0, f'Doctor registered successfully.', 'Doctor Registration')
            return redirect('/admin/AdminHomepage')
        else:
            win32api.MessageBox(0, 'User already exists with same email id.', 'Error')
            return redirect(request.referrer)
    else:
        return render_template("doctor_registration.html")

@app.route('/doctor/doctor_patient', methods=['GET', 'POST'])
def doctorpatient():
    if request.method == 'POST':
        doctor_id = request.form["user_id"]
        username = request.form["username"]
        patient= PatientModel.query.filter_by(email=username).first()
        patient_id=patient.id
        db.session.commit()

        if patient is None:
            win32api.MessageBox(0, f'Invalid patient email', 'Patient Email Error')
            return redirect(request.referrer)
        else:
            win32api.MessageBox(0, f'Valid Patient email', 'Patient Email')
            prescription=PrescriptionModel.query.filter_by(pid=str(patient_id)).first()
            prescription_id=prescription.id
            db.session.commit()
            return redirect(
                f'/doctor/DoctorComments?user_id={doctor_id}&prescription_Id={prescription.id}&mammogram_results={prescription.radiology_result}&radiologist_comments={prescription.radiology_comments}')
    else:
        user_id = request.args["id"]
        return render_template("doctor_patient.html", id=user_id)


@app.route('/doctor/DoctorComments', methods=['GET', 'POST'])
def doctor_comments():

    doctor_id = request.form["user_id"]
    prescription_id = request.form["prescription_Id"]
    doctor_comments = request.form["comments"]
    prescription_details = PrescriptionModel.query.filter_by(id=int(prescription_id)).first()
    if request.method == 'POST':

        if prescription_details is not None:
            prescription_details.did=doctor_id
            prescription_details.doctor_comments = doctor_comments
            db.session.commit()
            win32api.MessageBox(0, f'Successfully submitted doctor comments.', 'Alert')
            return redirect(f'/doctor/doctor_patient?id={prescription_details.did}')
        else:
            win32api.MessageBox(0, f'This patient have not done mammogram.', 'Alert')
            return redirect(request.referrer)
    else:
        doctor_id = request.args["user_id"]
        prescription_id = request.args["prescription_Id"]

        mammogram_result = request.args["mammogram_result"]
        radiologist_comments=request.args["radiologist_comments"]
        return render_template("doctorcomments.html", id=doctor_id, prescription_Id=prescription_id,
                               mammogram_result=mammogram_result, radiologist_comments=radiologist_comments)



# endregion

# region radiologist
@app.route('/radiologist/RadiologistLogin', methods=['GET', 'POST'])
def radiologist_login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = db.session.query(RadiologistModel).filter_by(email=username, password=password).first()
        db.session.commit()
        if user is None:
            win32api.MessageBox(0, f'Invalid email or password.', 'Login Error')
            return redirect(request.referrer)
        else:
            return redirect(f'/radiologist/UploadMammogram?id={user.id}')
    else:
        return render_template("radiologist_login.html")


@app.route('/radiologist/radiologistregistration', methods=['GET', 'POST'])
def radiologistregistration():
    if request.method == 'POST':
        data = request.form
        user = db.session.query(DoctorModel).filter_by(email=data['email']).first()
        db.session.commit()
        if user is None:
            new_radiologist = RadiologistModel(name=data['name'], DOB=data['dob'], phone_number=data['PhoneNumber'],
                                               specialization=data['specialization'], email=data['email'],
                                               password=data['password'])
            db.session.add(new_radiologist)
            db.session.commit()
            win32api.MessageBox(0, f'Radiologist registered successfully.', 'Radiologist Registration')
            return redirect('/admin/AdminHomepage')
        else:
            win32api.MessageBox(0, 'User already exists with same email id.', 'Error')
            return redirect(request.referrer)
    else:
        return render_template("radiologistregistrationpage.html")


@app.route('/radiologist/UploadMammogram', methods=['GET', 'POST'])
def upload_mammogram():
    if request.method == 'POST':
        radiologist_id = request.form["user_id"]
        username = request.form["email"]
        mammogram_file = request.files["mammogram_file"]

        user = db.session.query(PatientModel).filter_by(email=username).first()
        db.session.commit()

        if user is None:
            win32api.MessageBox(0, f'User does not exists.', 'Upload Error')
            return redirect(request.referrer)
        else:
            if mammogram_file:
                filename = secure_filename(mammogram_file.filename)
                file_extension = pathlib.Path(filename).suffix
                filename = f'{randomString()}{file_extension}'
                mammogram_file.save(Path(app.config['MAMMOGRAMS_PATH'], filename))
                res = Src.WebAPIs.ClassifyMammogram(f'{app.config["MAMMOGRAMS_PATH"]}{filename}')
                res = res.get_json(force=True)
                prescription = PrescriptionModel(pid=user.id, did='', rid=radiologist_id, patient_email=user.email,
                                                 radiology_result=res['result'], radiology_comments='',
                                                 radiology_image_path=filename, doctor_comments='')
                db.session.add(prescription)
                db.session.commit()
                return redirect(
                    f'/radiologist/RadiologistComments?prescription_Id={prescription.id}&mammogram_result={res["result"]}')

    else:
        user_id = request.args["id"]
        return render_template("radiologist_upload.html", id=user_id)


@app.route('/radiologist/RadiologistComments', methods=['GET', 'POST'])
def radiologist_comments():
    if request.method == 'POST':
        prescription_id = request.form["prescription_Id"]
        mammogram_comments = request.form["comments"]
        prescription_details = PrescriptionModel.query.filter_by(id=int(prescription_id)).first()
        if prescription_details is not None:
            prescription_details.radiology_comments = mammogram_comments
            db.session.commit()
            win32api.MessageBox(0, f'Successfully submitted mammogram comments.', 'Alert')
            return redirect(f'/radiologist/UploadMammogram?id={prescription_details.rid}')
    else:
        prescription_id = request.args["prescription_Id"]
        mammogram_result = request.args["mammogram_result"]
        return render_template("radilogistcomments.html", prescription_Id=prescription_id,
                               mammogram_result=mammogram_result)


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

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


if __name__ == "__main__":
    app.run(debug=False, threaded=False)
