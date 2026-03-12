from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    password = db.Column(db.String, nullable = False)
    
class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Text, primary_key = True)
    name = db.Column(db.Text, nullable = False)
    dob = db.Column(db.Date, nullable = False)  
    email = db.Column(db.Text, nullable = False, unique = True)
    education = db.Column(db.Text, nullable = False, default = 'None')
    skills = db.Column(db.Text, default = 'None')
    working_experience = db.Column(db.Integer, default = 0)

    application = db.relationship('Application', back_populates = 'student', cascade = 'all, delete-orphan')

class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, unique = True, nullable = False)
    hr_contact = db.Column(db.Text, unique = True, nullable = False)
    website = db.Column(db.Text, unique = True, nullable = False)
    approval_status = db.Column(db.Text, default = 'pending')
    location = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text, nullable = False)
    industry = db.Column(db.Text)

    placement_drive = db.relationship('PlacementDrive', back_populates = 'company', cascade = 'all, delete-orphan') 

class PlacementDrive(db.Model):
    __tablename__ = 'placement_drive'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'), nullable = False)
    job_title = db.Column(db.String, nullable = False)
    job_description = db.Column(db.String, nullable = False)
    eligibility = db.Column(db.String, nullable = False)
    deadline = db.Column(db.Date, nullable = False)
    status = db.Column(db.String, nullable = False, default = 'pending')
    salary = db.Column(db.Integer, nullable = False)

    company = db.relationship('Company', back_populates = 'placement_drive')
    application = db.relationship('Application', back_populates = 'placement_drive', cascade = 'all, delete-orphan')

class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    student_id = db.Column(db.String, db.ForeignKey('student.id', ondelete='CASCADE'), nullable = False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id', ondelete='CASCADE'), nullable = False)
    date = db.Column(db.Date, nullable = False)
    status = db.Column(db.String, default = 'applied')

    student = db.relationship('Student', back_populates = 'application')
    placement_drive = db.relationship('PlacementDrive', back_populates = 'application')