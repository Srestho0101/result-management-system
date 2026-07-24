from flask import Blueprint,redirect,url_for,render_template,session,flash
from app.models.teacher import AddStudentInfo
from app.routes.student.auth_check import student_roll_check

view_student_cgpa_bp = Blueprint(
    "view_student_cgpa",
    __name__,
    url_prefix="/view_student_cgpa"
)

@view_student_cgpa_bp.route("/")
def view_student_cgpa():
    student_roll_check()

    student_id = session.get("student_id")
    student_cgpa = AddStudentInfo.query.filter_by(student_id=student_id).first()

    return render_template("student/view_cgpa.html",student_cgpa=student_cgpa)