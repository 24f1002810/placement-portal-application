from flask import current_app as app, jsonify, request
from app import user_datastore
from flask_security import auth_required, current_user, hash_password, roles_required
from werkzeug.security import check_password_hash
import uuid
from models import *
from datetime import date

# Custom login endpoint that handles JSON requests
@app.route('/api/login', methods=['POST'])
def login():
    try:
        print(f"Login request received")
        
        data = request.get_json()
        print(f"Parsed JSON data: {data}")
        
        if not data:
            print("No JSON data provided")
            return jsonify({"response": {"message": "No JSON data provided"}}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        print(f"Email: {email}, Password provided: {password is not None}")

        if not email or not password:
            print("Email or password missing")
            return jsonify({"response": {"message": "Email and password are required"}}), 400

        user = User.query.filter_by(email=email).first()
        print(f"User found: {user is not None}")
        
        if not user:
            print(f"User with email {email} not found")
            return jsonify({"response": {"message": "Invalid email or password"}}), 400
        
        # Check password
        password_valid = check_password_hash(user.password, password)
        print(f"Password valid: {password_valid}")
        
        if not password_valid:
            print("Password does not match")
            return jsonify({"response": {"message": "Invalid email or password"}}), 400

        # Check if include_auth_token query parameter is present
        include_token = request.args.get('include_auth_token', 'false').lower() == 'true'
        
        if include_token:
            # Use the user's fs_uniquifier as the authentication token
            token = user.fs_uniquifier
            print(f"Token generated: {token[:10]}...")
            return jsonify({
                "response": {
                    "user": {
                        "authentication_token": token,
                        "email": user.email,
                        "id": user.id
                    },
                    "message": "Login successful"
                }
            }), 200
        else:
            return jsonify({"response": {"message": "Login successful"}}), 200
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Login error: {str(e)}")
        print(f"Traceback: {error_trace}")
        return jsonify({"response": {"message": f"Login error: {str(e)}"}}), 500

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
        profile_data['students'] = [student.to_dict() for student in Student.query.all()]
        profile_data['companies'] = [company.to_dict() for company in Company.query.all()]
        profile_data['drives'] = [drive.to_dict() for drive in PlacementDrive.query.all()]
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
    