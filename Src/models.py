from Util.database import db


class DoctorModel(db.Model):
    __tablename__ = 'doctor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    DOB = db.Column(db.Date())
    phone_number = db.Column(db.String())
    specialization = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, Name, DOB, PhoneNumber, specialization, email, password):
        self.Name = Name
        self.DOB = DOB
        self.PhoneNumber = PhoneNumber
        self.specialization = specialization
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<doctor {self.name}>"


class RadiologistModel(db.Model):
    __tablename__ = 'radiologist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    DOB = db.Column(db.Date())
    phone_number = db.Column(db.String())
    specialization = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, Name, DOB, PhoneNumber, specialization, email, password):
        self.Name = Name
        self.DOB = DOB
        self.PhoneNumber = PhoneNumber
        self.specialization = specialization
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<radiologist {self.name}>"


class AdminModel(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String())
    phone_number = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, name, address, phone_number, email, password):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<admin {self.name}>"


class PatientModel(db.Model):
    __tablename__ = 'patient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    DOB = db.Column(db.Date())
    guardian_name = db.Column(db.String())
    phone_number = db.Column(db.String())
    address = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, Name, DOB, Guardianname, PhoneNumber, Address, email, password):
        self.Name = Name
        self.DOB = DOB
        self.Guardianname = Guardianname
        self.PhoneNumber = PhoneNumber
        self.Address = Address
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<patient {self.name}>"


user_type_dict = {"doctor": DoctorModel, "patient": PatientModel, "radiologist": RadiologistModel}
