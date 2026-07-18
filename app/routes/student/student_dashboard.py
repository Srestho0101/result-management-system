from flask import Blueprint, render_template,session,flash,redirect,url_for
from app.models.teacher import AddStudentInfo
from app.routes.student.auth_check import student_roll_check

student_dashboard_bp = Blueprint(
    "student_dashboard",
    __name__,
    url_prefix="/student_dashboard"
)

@student_dashboard_bp.route("/")
def student_dashboard():
    student_roll_check()
    
    student_id = session.get("student_id")

    student_data = AddStudentInfo.query.filter_by(student_id=student_id).first()
    return render_template("student/student_dashboard.html",student_data=student_data)
