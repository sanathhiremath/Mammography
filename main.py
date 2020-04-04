import json
from flask import Flask,render_template,jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import win32api
#from validation import DoctorRegistrationForm
from flask_wtf import FlaskForm
from wtforms import  SubmitField, TextAreaField,Form, BooleanField, StringField, PasswordField, validators, TextField
from wtforms.validators import DataRequired, Email, InputRequired, Length
from flask_mail import Mail, Message





app=Flask(__name__)
app.config['SECRET_KEY'] = 'qwertyuiop'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:sneha@localhost:5432/Mammogram"
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'snehanarayan789@gmail.com'  # enter your email here
app.config['MAIL_DEFAULT_SENDER'] = 'snehanarayan789@gmail.com' # enter your email here
app.config['MAIL_PASSWORD'] = 'ambika1234'
db = SQLAlchemy(app)
mail = Mail(app)

migrate = Migrate(app, db)
x=[]

class DoctorModel(db.Model):
    __tablename__ = 'Doctor'


    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String())
    DOB = db.Column(db.Date())
    PhoneNumber = db.Column(db.String())
    specialization = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, Name, DOB, PhoneNumber, specialization, email, password):
        self.Name = Name
        self.DOB = DOB
        self.PhoneNumber = PhoneNumber
        self.specialization=specialization
        self.email=email
        self.password=password

    def __repr__(self):
        return f"<Doctor {self.name}>"

class RadiologistModel(db.Model):
    __tablename__ = 'Radiologist'


    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String())
    DOB = db.Column(db.Date())
    PhoneNumber = db.Column(db.String())
    specialization = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, Name, DOB, PhoneNumber, specialization, email, password):
        self.Name = Name
        self.DOB = DOB
        self.PhoneNumber = PhoneNumber
        self.specialization=specialization
        self.email=email
        self.password=password

    def __repr__(self):
        return f"<Radiologist {self.name}>"

class AdminModel(db.Model):
    __tablename__ = 'Admin'

    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String())
    Address = db.Column(db.String())
    PhoneNumber = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, Name, Address, PhoneNumber, email, password):
        self.Name = Name
        self.Address = Address
        self.PhoneNumber = PhoneNumber
        self.email=email
        self.password=password

    def __repr__(self):
        return f"<Admin {self.name}>"

class PatientModel(db.Model):
    __tablename__ = 'Patient'

    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String())
    DOB = db.Column(db.Date())
    Guardianname = db.Column(db.String())
    PhoneNumber = db.Column(db.String())
    Address = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, Name, DOB, Guardianname , PhoneNumber, Address, email, password):
        self.Name = Name
        self.DOB = DOB
        self.Guardianname = Guardianname
        self.PhoneNumber = PhoneNumber
        self.Address = Address
        self.email=email
        self.password=password

    def __repr__(self):
        return f"<Patient {self.name}>"

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
        if user is None :
            return render_template("homepage.html")
        elif password!=user.password:
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
            data=json.loads(y)

            #data = request.get_json()
            new_doctor = DoctorModel(Name=data['name'], DOB=data['dob'], PhoneNumber=data['PhoneNumber'], specialization=data['specialization'], email=data['email'], password=data['password'])

            db.session.add(new_doctor)
            db.session.commit()
            msg = Message("Confirmation Email", recipients=[new_doctor.email])
            msg.body = "You are successfully registered {} <{}>.".format(new_doctor.Name, new_doctor.email)
            msg.html=render_template("doctorresetpassword.html",username=new_doctor.Name, link="http://127.0.0.1:5000/doctor/passwordreset")
            mail.send(msg)
            return render_template("adminhomepage.html")
    else:
        return render_template("doctorregistration.html")

@app.route('/api/GetDoctorDetails/<email>/<password>', methods=['GET', 'POST'])
def GetDoctorDetails(email,password):
    #return "My emil is " +email+ " and password is "+ password
    #return "Hello"
    #json = request.get_json()
    value = db.session.query(DoctorModel).filter_by(email=email, password=password).first()
    #win32api.MessageBox(0, value.Name+value.email+str(value.DOB)+str(value.id)+value.PhoneNumber+value.specialization+value.password + " LoggedIn", 'Admin Response')

    db.session.commit()

    if value is None:
        r={"id":0}
        res={"result":r}
        result = json.dumps(res)
        #win32api.MessageBox(0,"invalid",'Admin response')
        return result
    else:
        v={"id":int(value.id), "name":value.Name, "dob":str(value.DOB), "phonenumber":value.PhoneNumber,"specialization":value.specialization, "email":value.email, "password": value.password}
        res={"result":v}
        #win32api.MessageBox(0,str(v),'Admin Response')

        result=json.dumps(res)
        #result=Response(js, status=200, mimetype=)
        #win32api.MessageBox(0, value.Name + " LoggedIn", 'Admin Response')
        return result


@app.route('/radiologist', methods=['GET', 'POST'])
def radiologist():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        user = db.session.query(RadiologistModel).filter_by(email=username).first()

        db.session.commit()
        if user is None :
            return render_template("homepage.html")
        elif password!=user.password:
            return render_template("homepage.html")
        else:
            return render_template("radiologistregistrationpage.html")
    else:
        return render_template("radiologisthomepage.html")

@app.route('/radiologist/radiologistregistration', methods=['GET', 'POST'])
def radiologistregistration():

    if request.method == 'POST':


            re=json.dumps(request.form)
            r=json.loads(re)

            #data = request.get_json()
            new_radiologist = RadiologistModel(Name=r['name'], DOB=r['dob'], PhoneNumber=r['PhoneNumber'], specialization=r['specialization'], email=r['email'], password=r['password'])
            db.session.add(new_radiologist)
            db.session.commit()
            return render_template("adminhomepage.html")
    else:
        return render_template("radiologistregistrationpage.html")

#@app.route('/admin', methods=['GET', 'POST'])
#def admin():
        #return render_template("adminlogin.html")


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

            pa=json.dumps(request.form)
            p=json.loads(pa)

            #data = request.get_json()
            new_patient = PatientModel(Name=p['name'],DOB=p['dob'], Guardianname=p['guardianname'], PhoneNumber=p['PhoneNumber'],Address=p['address'], email=p['email'], password=p['password'])
            db.session.add(new_patient)
            db.session.commit()
            message="Successfully Registered"
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
        if user is None :
            return render_template("homepage.html")
        elif password!=user.password:
            return render_template("homepage.html")
        else:
            return render_template("radiologistregistrationpage.html")
    else:
        return render_template("patienthomepage.html")




if __name__=="__main__":

    app.run(host='0.0.0.0', debug=True)
