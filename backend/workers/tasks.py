from workers.celery_worker import celery_app
from celery.schedules import crontab
from models import db, Company, PlacementDrive, Application, Student
from datetime import datetime, timedelta
import requests
from flask import current_app
import csv
import os

@celery_app.task
def send_monthly_placement_updates():
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

    companies = Company.query.filter_by(approval_status='approved').all()
    
    webhook_url = current_app.config.get('WEBHOOK_URL')
    
    results = []
    
    for company in companies:
        drives = PlacementDrive.query.filter_by(company_id=company.id).all()
        drive_ids = [d.id for d in drives]
        
        drives_conducted = len(drives)
        
        apps = Application.query.filter(Application.drive_id.in_(drive_ids)).all()
        
        apps_last_month = [
            app for app in apps 
            if app.date and first_day_of_previous_month.date() <= app.date <= last_day_of_previous_month.date()
        ]
        
        total_apps = len(apps)
        apps_this_month_count = len(apps_last_month)
        
        selected_apps = [
            app for app in apps 
            if app.status.lower() == 'placed'
        ]
        total_selected = len(selected_apps)
        
        payload = {
            "company_id": company.id,
            "company_name": company.name,
            "email": company.user_account.email if company.user_account else None,
            "report_month": first_day_of_previous_month.strftime("%B %Y"),
            "monthly_applications": apps_this_month_count,
            "total_applications": total_apps,
            "total_students_selected": total_selected,
            "total_drives_conducted": drives_conducted
        }
        
        if webhook_url:
            try:
                response = requests.post(webhook_url, json=payload, timeout=5)
                results.append({"company": company.name, "status": response.status_code})
            except Exception as e:
                results.append({"company": company.name, "error": str(e)})

    return results

@celery_app.task
def update_closed_drives():
    today = datetime.today().date()
    
    drives = PlacementDrive.query.filter(PlacementDrive.deadline < today, PlacementDrive.status != 'closed').all()
    
    count = 0
    for drive in drives:
        drive.status = 'closed'
        count += 1
        
    if count > 0:
        db.session.commit()
        
    return f"Updated {count} placement drives to closed status."

@celery_app.task
def send_interview_reminders():
    # Tomorrow's date
    tomorrow = (datetime.today() + timedelta(days=1)).date()
    
    # Get all applications with an interview tomorrow
    upcoming_interviews = Application.query.filter(
        Application.interview_date == tomorrow,
        Application.status != 'rejected',
        Application.status != 'placed'
    ).all()
    
    webhook_url = current_app.config.get('WEBHOOK_URL')
    results = []
    
    for app in upcoming_interviews:
        student = app.student
        drive = app.placement_drive
        company = drive.company
        
        payload = {
            "type": "interview_reminder",
            "student_id": student.id,
            "student_email": student.user_account.email if student.user_account else None,
            "company_name": company.name,
            "job_title": drive.job_title,
            "interview_date": app.interview_date.isoformat(),
            "message": f"Reminder: You have an upcoming interview with {company.name} for the {drive.job_title} role tomorrow!"
        }
        
        if webhook_url:
            try:
                response = requests.post(webhook_url, json=payload, timeout=5)
                results.append({"student": student.name, "company": company.name, "status": response.status_code})
            except Exception as e:
                results.append({"student": student.name, "company": company.name, "error": str(e)})
                
    return results

celery_app.conf.beat_schedule = {
    'send-monthly-updates': {
        'task': 'workers.tasks.send_monthly_placement_updates',
        'schedule': crontab(day_of_month='1', hour='0', minute='0'),
    },
    'update-closed-drives': {
        'task': 'workers.tasks.update_closed_drives',
        'schedule': crontab(hour='0', minute='5'),
    },
    'send-interview-reminders': {
        'task': 'workers.tasks.send_interview_reminders',
        'schedule': crontab(hour='20', minute='2'),
    }
}

@celery_app.task(bind=True)
def export_student_applications(self, student_id):
    student = Student.query.get(student_id)
    if not student:
        return {"status": "error", "message": "Student not found"}
        
    apps = Application.query.filter_by(student_id=student_id).all()
    
    downloads_dir = os.path.join(current_app.instance_path, 'downloads')
    os.makedirs(downloads_dir, exist_ok=True)
    
    filename = f"applications_{self.request.id}.csv"
    filepath = os.path.join(downloads_dir, filename)
    
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Company', 'Job Title', 'Applied On', 'Interview Date', 'Status'])
        
        for app in apps:
            company_name = app.placement_drive.company.name if app.placement_drive and app.placement_drive.company else 'Unknown'
            job_title = app.placement_drive.job_title if app.placement_drive else 'Unknown'
            applied_on = app.date.isoformat() if app.date else 'N/A'
            interview_date = app.interview_date.isoformat() if app.interview_date else 'N/A'
            status = app.status
            
            writer.writerow([company_name, job_title, applied_on, interview_date, status])
            
    return {"status": "success", "filename": filename}