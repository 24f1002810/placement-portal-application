from flask import current_app as app, jsonify, request
from app import user_datastore
import uuid
from models import *
from datetime import date
from flask_security import auth_required, current_user, hash_password, roles_required

# NOTE: The /api/login route has been removed!
# To login, simply POST JSON to: http://localhost:5000/login?include_auth_token=true
# Body: {"email": "admin@example.com", "password": "password123"}

@app.route('/api/dashboard', methods=['POST', 'GET'])
@auth_required('token')
def dashboard():
    roles = [role.name for role in current_user.roles]
    profile_data = {
        "user_id": current_user.id,
        "email": current_user.email,
        "roles": roles
    }

    if 'student' in roles:
        profile_data['name'] = current_user.student_profile.name
        # Convert skills from string to array
        skills_str = current_user.student_profile.skills or ''
        profile_data['skills'] = [s.strip() for s in skills_str.split(',') if s.strip()]
        profile_data['applications'] = [
            {
                'id': app.id,
                'drive_id': app.drive_id,
                'date': app.date.isoformat() if app.date else None,
                'status': app.status
            } for app in current_user.student_profile.application
        ]
        return jsonify({ "profile": profile_data, 'message': "Welcome to the Student Dashboard"})
    elif 'company' in roles:
        profile_data['company_name'] = current_user.company_profile.name
        profile_data['industry'] = current_user.company_profile.industry
        profile_data['description'] = current_user.company_profile.description
        profile_data['drives'] = [
            {
                'id': drive.id,
                'job_title': drive.job_title,
                'job_description': drive.job_description,
                'eligibility': drive.eligibility,
                'deadline': drive.deadline.isoformat() if drive.deadline else None,
                'status': drive.status,
                'salary': drive.salary
            } for drive in current_user.company_profile.placement_drive
        ]

        return jsonify({ "profile": profile_data, 'message': "Welcome to the Company Dashboard"})
    elif 'admin' in roles:
        return jsonify({ "profile": profile_data, 'message': "Welcome to the Admin Dashboard"})
    else:
        return jsonify({"message": "Unknown role"}), 400


@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        if not email or not password or not role:
            return jsonify({"message": "Email, password, and role are required"}), 400

        if role not in ['student', 'company']:
            return jsonify({"message": "Role must be either 'student' or 'company'"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email already registered"}), 400

        new_user = User(
            email=email,
            password=hash_password(password),
            fs_uniquifier=uuid.uuid4().hex
        )
        db.session.add(new_user)
        db.session.flush()  # Flush to get the new user's ID

        user_datastore.add_role_to_user(new_user, role)

        if role == 'student':
            student_profile = Student(
                user_id=new_user.id,
                name=data.get('name'),
                phone_number=data.get('phone'),
                dob=date.fromisoformat(data.get('dob'))
            )
            db.session.add(student_profile)
        elif role == 'company':
            company_profile = Company(
                user_id=new_user.id,
                name=data.get('companyName'),
                industry=data.get('industry'),
                website=data.get('website'),
                hr_contact=data.get('hrContact'),
                location=data.get('location'),
                description=data.get('description')
            )
            db.session.add(company_profile)

        db.session.commit()
        return jsonify({"message": f"User registered successfully as {role}"}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {str(e)}")
        return jsonify({"message": f"Registration error: {str(e)}"}), 500

@app.route('/api/admin', methods=['POST'])
@auth_required('token')
@roles_required('admin')
def admin():
    return jsonify({"message": "Welcome to the Admin Dashboard"})
    