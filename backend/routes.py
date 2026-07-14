from flask import current_app as app, jsonify, request
from app import user_datastore
from flask_security import auth_required, current_user, hash_password, roles_required, roles_accepted
from flask_security.utils import verify_password
import uuid
from models import *
from datetime import date
import admin, company, student

@app.route('/logout', methods=['POST'])
@auth_required('token')
def logout():
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
        profile_data['student_id'] = current_user.student_profile.id
        skills_str = current_user.student_profile.skills or ''
        profile_data['skills'] = [s.strip() for s in skills_str.split(',') if s.strip()]
        profile_data['applications'] = [app.to_dict() for app in current_user.student_profile.application]
        profile_data['role'] = 'student'
        return jsonify({ "profile": profile_data, 'message': "Welcome to the Student Dashboard"})

    elif 'company' in roles:
        profile_data['company_id'] = current_user.company_profile.id
        profile_data['company_name'] = current_user.company_profile.name
        profile_data['industry'] = current_user.company_profile.industry
        profile_data['description'] = current_user.company_profile.description
        profile_data['approval_status'] = current_user.company_profile.approval_status
        profile_data['drives'] = [drive.to_dict() for drive in current_user.company_profile.placement_drive]
        profile_data['role'] = 'company'
        return jsonify({ "profile": profile_data, 'message': "Welcome to the Company Dashboard"})
        
    elif 'admin' in roles:
        profile_data['student_count'] = Student.query.count()
        profile_data['company_count'] = Company.query.filter_by(approval_status='approved').count()
        profile_data['drive_count'] = PlacementDrive.query.filter_by(status='approved').count()
        profile_data['role'] = 'admin'
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
        db.session.flush() 
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
        drive_dict = drive.to_dict()
        if current_user.has_role('student') and current_user.student_profile:
            app_inst = Application.query.filter_by(student_id=current_user.student_profile.id, drive_id=drive_id).first()
            drive_dict['has_applied'] = bool(app_inst)
            if app_inst:
                drive_dict['application_id'] = app_inst.id
        return jsonify({"drive": drive_dict})

    elif request.method == 'POST':
        data = request.get_json()
        
        if 'status' in data:
            drive.status = data['status']
            db.session.commit()
            return jsonify({"message": f"Drive status updated to {data['status']}"})

        elif 'deadline' in data and data['deadline']:
            try:
                from datetime import date
                data['deadline'] = date.fromisoformat(data['deadline'])
            except ValueError:
                pass

            for key, value in data.items():
                setattr(drive, key, value)
            db.session.commit()
            return jsonify({"message": "Placement Drive updated"})

    elif request.method == 'DELETE' and (current_user.has_role('admin') or current_user.has_role('company')):
        db.session.delete(drive)
        db.session.commit()
        return jsonify({"message": "Placement Drive successfully deleted"})
        
@app.route('/api/placement-drive/<int:drive_id>/apply', methods=['POST'])
@auth_required()
@roles_accepted('student')
def apply_to_drive(drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({"message": "Placement Drive not found"}), 404
        
    student_id = current_user.student_profile.id
    existing_app = Application.query.filter_by(student_id=student_id, drive_id=drive_id).first()
    if existing_app:
        return jsonify({"message": "Already applied to this drive"}), 400
        
    new_app = Application(
        student_id=student_id,
        drive_id=drive_id,
        date=date.today(),
        status='applied'
    )
    db.session.add(new_app)
    db.session.commit()
    return jsonify({"message": "Successfully applied to drive", "application_id": new_app.id}), 200
    
    
@app.route('/api/application/<int:app_id>', methods=['GET', 'POST', 'DELETE'])
@auth_required()
@roles_accepted('admin', 'company', 'student')
def manage_application(app_id):
    application = Application.query.get(app_id)
    if not application:
        return jsonify({"message": "Application not found"}), 404

    if request.method == 'GET':
        app_dict = application.to_dict()
        app_dict['student_details'] = application.student.to_dict()
        app_dict['drive_details'] = application.placement_drive.to_dict()
        return jsonify({"application": app_dict})

    elif request.method == 'POST':

        data = request.get_json()
        if 'status' in data:
            application.status = data['status']
        if 'interview_date' in data:
            val = data['interview_date']
            if val:
                from datetime import datetime
                if 'T' in val:
                    val = val.split('T')[0]
                if ' ' in val:
                    val = val.split(' ')[0]
                try:
                    application.interview_date = date.fromisoformat(val)
                except ValueError:
                    return jsonify({"message": "Invalid date format"}), 400
            else:
                application.interview_date = None
        db.session.commit()
        return jsonify({
            "message": "Application updated",
            "status": application.status,
            "interview_date": application.interview_date.isoformat() if application.interview_date else None
        })
        return jsonify({"message": "No status provided"}), 400

    elif request.method == 'DELETE' and current_user.has_role('admin'):
        db.session.delete(application)
        db.session.commit()
        return jsonify({"message": "Application deleted successfully"})