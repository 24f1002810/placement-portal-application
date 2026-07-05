from flask import current_app as app, request, jsonify
from flask_security import auth_required, current_user, roles_required, roles_accepted
from models import *

@app.route('/api/company/<int:company_id>', methods=['GET', 'POST', 'DELETE'])
@auth_required()
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

@app.route('/api/company/<int:company_id>/placement-drives', methods=['GET'])
@auth_required()
def get_company_placement_drives(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found"}), 404

    # Check if the current user is the owner of the company or an admin
    if current_user.id != company.user_id and 'admin' not in [role.name for role in current_user.roles]:
        return jsonify({"message": "Unauthorized access"}), 403

    placement_drives = PlacementDrive.query.filter_by(company_id=company_id).all()
    return jsonify({"placement_drives": [drive.to_dict() for drive in placement_drives]})