from flask import current_app as app, request, jsonify
from flask_security import auth_required, roles_accepted, roles_required, current_user
from models import *
from datetime import date

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

    elif request.method == 'DELETE' and (current_user.has_role('admin') or current_user.has_role('student')):
        user = User.query.get(student.user_id)
        db.session.delete(student)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Student profile deleted"})

@app.route('/api/student/<int:student_id>/applications', methods=['GET', 'DELETE'])
@auth_required()
@roles_accepted('admin', 'student')
def student_applications(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404
    
    if request.method == 'GET':
        applications = []
        for app in student.application:
            app_dict = app.to_dict()
            app_dict['company_name'] = app.placement_drive.company.name if app.placement_drive and app.placement_drive.company else 'Unknown'
            app_dict['job_title'] = app.placement_drive.job_title if app.placement_drive else 'Unknown'
            applications.append(app_dict)
        return jsonify({'applications': applications})

@app.route('/api/student/placement-drives', methods=['GET'])
@auth_required()
@roles_accepted('admin', 'student')
def student_placement_drives():
    drives = PlacementDrive.query.filter_by(status='approved').all()
    return jsonify({"drives": [drive.to_dict() for drive in drives]})