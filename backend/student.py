from flask import current_app as app, request, jsonify, send_file
from flask_security import auth_required, roles_accepted, roles_required, current_user
from models import *
from datetime import date
from cache import cache
import os
from celery.result import AsyncResult

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
@cache.cached(timeout=180)
def student_placement_drives():
    drives = PlacementDrive.query.filter_by(status='approved').all()
    return jsonify({"drives": [drive.to_dict() for drive in drives]})

@app.route('/api/student/<int:student_id>/export_applications', methods=['POST'])
@auth_required()
@roles_accepted('student')
def export_applications(student_id):
    if current_user.student_profile.id != student_id:
        return jsonify({"message": "Unauthorized"}), 403
        
    from workers.tasks import export_student_applications
    task = export_student_applications.delay(student_id)
    return jsonify({"task_id": task.id}), 202

@app.route('/api/task_status/<task_id>', methods=['GET'])
@auth_required()
@roles_accepted('student')
def task_status(task_id):
    from workers.celery_worker import celery_app
    task = AsyncResult(task_id, app=celery_app)
    if task.state == 'PENDING':
        response = {"state": task.state, "status": "Pending..."}
    elif task.state != 'FAILURE':
        response = {"state": task.state, "result": task.info}
    else:
        response = {"state": task.state, "status": str(task.info)}
    return jsonify(response)

@app.route('/api/download/<task_id>', methods=['GET'])
def download_file(task_id):
    downloads_dir = os.path.join(app.instance_path, 'downloads')
    filename = f"applications_{task_id}.csv"
    filepath = os.path.join(downloads_dir, filename)
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({"message": "File not found"}), 404