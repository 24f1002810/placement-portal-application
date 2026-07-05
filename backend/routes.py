from flask import current_app as app, jsonify, request
from app import user_datastore
from flask_security import auth_required, current_user, hash_password, roles_required, roles_accepted
from flask_security.utils import verify_password
import uuid
from models import *
from datetime import date
import admin, company

@app.route('/logout', methods=['POST'])
@auth_required('token')
def logout():
    # Invalidate the current user's session by changing the fs_uniquifier
    current_user.fs_uniquifier = uuid.uuid4().hex
    db.session.commit()
    return jsonify({"message": "Logged out successfully"}), 200

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
        profile_data['applications'] = [app.to_dict() for app in current_user.student_profile.application]
        return jsonify({ "profile": profile_data, 'message': "Welcome to the Student Dashboard"})
    elif 'company' in roles:
        profile_data['company_name'] = current_user.company_profile.name
        profile_data['industry'] = current_user.company_profile.industry
        profile_data['description'] = current_user.company_profile.description
        profile_data['drives'] = [drive.to_dict() for drive in current_user.company_profile.placement_drive]

        return jsonify({ "profile": profile_data, 'message': "Welcome to the Company Dashboard"})
    elif 'admin' in roles:
        profile_data['student_count'] = Student.query.count()
        profile_data['company_count'] = Company.query.filter_by(approval_status='approved').count()
        profile_data['drive_count'] = PlacementDrive.query.filter_by(status='approved').count()
        
        profile_data['application_count'] = db.session.query(Application).join(
            PlacementDrive, Application.drive_id == PlacementDrive.id
        ).filter(
            PlacementDrive.status == 'approved',
        ).count()

        profile_data['pending_company_registrations'] = Company.query.filter_by(approval_status='pending').count()
        profile_data['pending_drives'] = PlacementDrive.query.filter_by(status='pending').count()
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
                hr_phone=data.get('hrContact'),
                location=data.get('location'),
                description=data.get('description')
            )
            db.session.add(company_profile)

        db.session.commit()
        return jsonify({"message": f"User registered successfully as {role}"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {str(e)}")
        return jsonify({"message": "Registration error"}), 500


@app.route('/api/placement-drive/<int:drive_id>', methods=['GET', 'POST', 'DELETE'])
@auth_required()
@roles_accepted('admin', 'company', 'student')
def manage_drive(drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({"message": "Placement Drive not found"}), 404

    if request.method == 'GET':
        return jsonify({"drive": drive.to_dict()})

    elif request.method == 'POST':
        data = request.get_json()
        if 'deadline' in data and data['deadline']:
            try:
                from datetime import date
                data['deadline'] = date.fromisoformat(data['deadline'])
            except ValueError:
                pass # let it fail or handle if it's already a date/invalid

        # Update drive attributes based on data
        for key, value in data.items():
            setattr(drive, key, value)
        db.session.commit()
        return jsonify({"message": "Placement Drive updated"})

    elif request.method == 'DELETE' and (current_user.has_role('admin') or current_user.has_role('company')):
        db.session.delete(drive)
        db.session.commit()
        return jsonify({"message": "Placement Drive successfully deleted"})
    
    
@app.route('/api/student/<int:student_id>', methods=['GET', 'POST', 'DELETE'])
@auth_required()
@roles_accepted('admin', 'student', 'company')
def get_student_profile(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404
    
    if request.method == 'GET':
        student_data = student.to_dict()
        student_data['dob'] = student.dob.isoformat() if student.dob else None 
        student_data['blocked'] = not student.user_account.active
        return jsonify({"student": student_data})
    
    elif request.method == 'POST':
        data = request.get_json()
        dob = date.fromisoformat(data.get('dob')) if data.get('dob') else None

        if data.get('block') is not None:
            block = data.get('block')
            if block:
                student.user_account.active = 0
                db.session.commit()
                return jsonify({"message": "Student account blocked"})
            else:
                student.user_account.active = 1
                db.session.commit()
                return jsonify({"message": "Student account unblocked"})
        else:
            for key, value in data.items():
                if key == 'dob':
                    setattr(student, key, dob)
                else:
                    setattr(student, key, value)
            db.session.commit()
            return jsonify({"message": "Student profile updated"})

    elif request.method == 'DELETE' and (current_user.has_role('admin') or current_user.has_role('company')):
        user = User.query.get(student.user_id)
        db.session.delete(student)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Student profile deleted"})