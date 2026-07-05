from flask import current_app as app, request, jsonify
from flask_security import auth_required, current_user, roles_required, roles_accepted
from models import *

@app.route('/api/admin', methods=['POST'])
@auth_required('token')
@roles_required('admin')
def admin():
    return jsonify({"message": "Welcome to the Admin Dashboard"})


@app.route('/api/registration-requests', methods=['GET', 'POST'])
@auth_required()
@roles_required('admin')
def handle_registration_requests():
    if request.method == 'GET':
        pending_companies = Company.query.filter_by(approval_status='pending').all()
        return jsonify({"pending_companies": [c.to_dict() for c in pending_companies]})
    
    elif request.method == 'POST':
        data = request.get_json()
        company_id = data.get('company_id')
        action = data.get('action')  # 'approve' or 'reject'
        
        company = Company.query.get(company_id)
        if not company:
            return jsonify({"message": "Company not found"}), 404
        
        if action == 'approve':
            company.approval_status = 'approved'
            db.session.commit()
            return jsonify({"message": "Company approved"})
        elif action == 'reject':
            db.session.delete(company)
            db.session.commit()
            return jsonify({"message": "Company rejected"})
        else:
            return jsonify({"message": "Invalid action"}), 400
        
@app.route('/api/drive-requests', methods=['GET', 'POST'])
@auth_required()
@roles_required('admin')
def handle_drive_requests():
    if request.method == 'GET':
        pending_drives = PlacementDrive.query.filter_by(status='pending').all()
        return jsonify({"pending_drives": [d.to_dict() for d in pending_drives]})
    
    elif request.method == 'POST':
        data = request.get_json()
        drive_id = data.get('drive_id')
        action = data.get('action')  # 'approve' or 'reject'
        
        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return jsonify({"message": "Placement Drive not found"}), 404
        
        if action == 'approve':
            drive.status = 'approved'
            db.session.commit()
            return jsonify({"message": "Placement Drive approved"})
        elif action == 'reject':
            db.session.delete(drive)
            db.session.commit()
            return jsonify({"message": "Placement Drive rejected"})
        else:
            return jsonify({"message": "Invalid action"}), 400

@app.route('/api/admin/students', methods=['GET'])
@auth_required()
@roles_required('admin')
def get_all_students():
    try:
        students = Student.query.all()
        return jsonify({
            "students": [student.to_dict() for student in students],
            "total": len(students)
        })
    except Exception as e:
        return jsonify({"message": f"Error fetching students: {str(e)}"}), 500

@app.route('/api/admin/companies', methods=['GET'])
@auth_required()
@roles_required('admin')
def get_all_companies():
    try:
        companies = Company.query.all()
        return jsonify({
            "companies": [company.to_dict() for company in companies],
            "total": len(companies)
        })
    except Exception as e:
        return jsonify({"message": f"Error fetching companies: {str(e)}"}), 500

@app.route('/api/admin/placement-drives', methods=['GET'])
@auth_required()
@roles_required('admin')
def get_all_drives():
    try:
        drives = PlacementDrive.query.all()
        return jsonify({
            "placement_drives": [drive.to_dict() for drive in drives],
            "total": len(drives)
        })
    except Exception as e:
        return jsonify({"message": f"Error fetching placement drives: {str(e)}"}), 500
