from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

roles_users = db.Table('roles_users',
                       db.Column('user_id',db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    student_profile = db.relationship('Student', backref='user_account', uselist=False, cascade="all, delete-orphan")
    company_profile = db.relationship('Company', backref='user_account', uselist=False, cascade="all, delete-orphan")
    
class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    name = db.Column(db.Text, nullable = False)
    dob = db.Column(db.Date, nullable = False)  
    phone_number = db.Column(db.String(15), unique = True, nullable = False)
    education = db.Column(db.Text, default = 'None')
    skills = db.Column(db.Text, default = 'None')
    working_experience = db.Column(db.Integer, default = 0)
    cgpa = db.Column(db.Float, default = 0.0)

    application = db.relationship('Application', back_populates = 'student', cascade = 'all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.user_account.email,
            'phone_number': self.phone_number,
            'cgpa': self.cgpa,
            'skills': [s.strip() for s in (self.skills or '').split(',') if s.strip()],
            'education': self.education,
            'active': self.user_account.active if self.user_account else True
        }

class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    name = db.Column(db.Text, unique = True, nullable = False)
    hr_phone = db.Column(db.Text, unique = True, nullable = False)
    website = db.Column(db.Text, unique = True, nullable = False)
    approval_status = db.Column(db.Text, default = 'pending')
    location = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text, nullable = False)
    industry = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'industry': self.industry,
            'location': self.location,
            'approval_status': self.approval_status,
            'description': self.description,
            'website': self.website,
            'hr_phone': self.hr_phone,
            'email': self.user_account.email,
            'active': self.user_account.active
        }
    placement_drive = db.relationship('PlacementDrive', back_populates = 'company', cascade = 'all, delete-orphan') 

class PlacementDrive(db.Model):
    __tablename__ = 'placement_drive'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'), nullable = False)
    job_title = db.Column(db.String, nullable = False)
    job_description = db.Column(db.String, nullable = False)
    skills_required = db.Column(db.String, nullable = False)
    min_cgpa = db.Column(db.Float, nullable = False)
    working_experience_required = db.Column(db.Integer, nullable = False)

    deadline = db.Column(db.Date, nullable = False)
    status = db.Column(db.String, nullable = False, default = 'pending')
    salary = db.Column(db.Integer, nullable = False)

    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'company_name': self.company.name,
            'job_title': self.job_title,
            'job_description': self.job_description,
            'skills_required': self.skills_required,
            'min_cgpa': self.min_cgpa,
            'working_experience_required': self.working_experience_required,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'status': self.status,
            'salary': self.salary,
            'application_count': len(self.application) if self.application else 0
        }
    
    company = db.relationship('Company', back_populates = 'placement_drive')
    application = db.relationship('Application', back_populates = 'placement_drive', cascade = 'all, delete-orphan')

    
class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    student_id = db.Column(db.String, db.ForeignKey('student.id', ondelete='CASCADE'), nullable = False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id', ondelete='CASCADE'), nullable = False)
    date = db.Column(db.Date, nullable = False)
    status = db.Column(db.String, default = 'applied')
    interview_date = db.Column(db.Date, nullable = True)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'drive_id': self.drive_id,
            'date': self.date.isoformat() if self.date else None,
            'status': self.status,
            'interview_date': self.interview_date.isoformat() if self.interview_date else None
        }

    student = db.relationship('Student', back_populates = 'application')
    placement_drive = db.relationship('PlacementDrive', back_populates = 'application')