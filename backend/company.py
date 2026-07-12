from flask import current_app as app, request, jsonify
from flask_security import auth_required, roles_accepted
from models import *
from datetime import date

@app.route('/api/company/<int:company_id>', methods=['GET', 'POST', 'DELETE'])
@auth_required()
@roles_accepted('admin', 'company')
def view_company_details(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found"}), 404
    
    if request.method == 'GET':
        return jsonify({"company": company.to_dict()})
    
    elif request.method == 'POST':
        data = request.get_json()

        if data.get('block') is not None:
            block = data.get('block')
            if block == True:
                company.user_account.active = 0
                db.session.commit()
                return jsonify({'message':"Company blocked successfully"})
            else:
                company.user_account.active = 1
                db.session.commit()
                return jsonify({'message':"Company unblocked successfully"})

        for key, value in data.items():
            setattr(company, key, value)
        db.session.commit()
        return jsonify({"message": "Company details updated"}), 200
    
    elif request.method == 'DELETE':
        user = User.query.get(company.user_id)
        db.session.delete(company)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Company successfully deleted"}), 200

@app.route('/api/company/<int:company_id>/placement-drives', methods=['GET', 'POST'])
@auth_required()
@roles_accepted('admin', 'company')
def get_company_placement_drives(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found"}), 404

    if request.method == 'GET':
        placement_drives = PlacementDrive.query.filter_by(company_id=company_id).all()
        return jsonify({"placement_drives": [drive.to_dict() for drive in placement_drives]})
        
    elif request.method == 'POST':
        data = request.get_json()
        
        job_title = data.get('job_title', '').strip()
        
        # Check if an active drive with the same job role already exists
        existing_drive = PlacementDrive.query.filter(
            PlacementDrive.company_id == company_id,
            PlacementDrive.job_title.ilike(job_title),
            PlacementDrive.status.in_(['pending', 'approved'])
        ).first()

        if existing_drive:
            return jsonify({"message": f"An active placement drive for '{job_title}' already exists."}), 400
            
        try:
            deadline = date.fromisoformat(data['deadline'])
        except (ValueError, TypeError):
            return jsonify({"message": "Invalid date format for deadline"}), 400
            
        new_drive = PlacementDrive(
            company_id=company_id,
            job_title=data.get('job_title'),
            job_description=data.get('job_description'),
            skills_required=data.get('skills_required'),
            min_cgpa=data.get('min_cgpa'),
            working_experience_required=data.get('working_experience_required'),
            deadline=deadline,
            salary=data.get('salary'),
            status='pending'  # Automatically pending admin approval
        )
        db.session.add(new_drive)
        db.session.commit()
        return jsonify({"message": "Placement drive requested successfully", "drive": new_drive.to_dict()}), 201

@app.route('/api/company/<int:company_id>/applications', methods=['GET'])
@auth_required()
@roles_accepted('admin', 'company')
def get_company_applications(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found"}), 404

    # Get all placement drives for this company
    drive_ids = [drive.id for drive in company.placement_drive]
    
    # Get all applications for those drives
    applications = Application.query.filter(Application.drive_id.in_(drive_ids)).all()
    
    result = []
    for app_instance in applications:
        app_dict = app_instance.to_dict()
        app_dict['student_name'] = app_instance.student.name if app_instance.student else 'Unknown'
        app_dict['job_title'] = app_instance.placement_drive.job_title if app_instance.placement_drive else 'Unknown'
        app_dict['company_name'] = company.name
        result.append(app_dict)
        
    return jsonify({
        "applications": result,
        "total": len(result)
    })