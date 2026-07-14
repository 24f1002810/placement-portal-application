import uuid
from datetime import date
from app import app, user_datastore
from models import db, Student, Company
from flask_security import hash_password

def setup_database():
    with app.app_context():
        print("Creating tables...")
        db.create_all()

        print("Setting up roles...")
        user_datastore.find_or_create_role(name='admin')
        user_datastore.find_or_create_role(name='student')
        user_datastore.find_or_create_role(name='company')
        db.session.commit()

        print("Creating Admin user...")
        if not user_datastore.find_user(email="admin@test.com"):
            user_datastore.create_user(
                email="admin@test.com",
                password=hash_password("admin123"),
                fs_uniquifier=uuid.uuid4().hex,
                roles=['admin']
            )

        print("Creating Student user and profile...")
        if not user_datastore.find_user(email="student@test.com"):
            student_user = user_datastore.create_user(
                email="student@test.com",
                password=hash_password("student123"),
                fs_uniquifier=uuid.uuid4().hex,
                roles=['student']
            )
            db.session.flush() 
            
            student_profile = Student(
                user_id=student_user.id,
                name="Jane Doe",
                dob=date(2002, 5, 14),
                education="B.Tech Computer Science",
                skills="Python, Flask, React",
                working_experience = 1,
                cgpa = 8.5,
                phone_number = "8000413113"
            )
            db.session.add(student_profile)

        print("Creating Company user and profile...")
        if not user_datastore.find_user(email="company@test.com"):
            company_user = user_datastore.create_user(
                email="company@test.com",
                password=hash_password("company123"),
                fs_uniquifier=uuid.uuid4().hex,
                roles=['company']
            )
            db.session.flush()

            company_profile = Company(
                user_id=company_user.id,
                name="Acme Corp",
                hr_phone="8000413114",
                website="www.acmecorp.com",
                location="Udaipur, Rajasthan",
                description="Innovative software solutions provider.",
                industry="IT Services",
            )
            db.session.add(company_profile)

        db.session.commit()
        print("Database successfully initialized!")

if __name__ == '__main__':
    setup_database()