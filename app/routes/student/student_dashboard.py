from flask import Blueprint, render_template,session,flash,redirect,url_for
from app.models.teacher import AddStudentInfo

student_dashboard_bp = Blueprint(
    "student_dashboard",
    __name__,
    url_prefix="/student_dashboard"
)

@student_dashboard_bp.route("/")
def student_dashboard():
    if not session.get("student"):
        flash("Please login first","danger")
        return redirect(url_for("home.home"))
    
    student_id = session.get("student_id")

    student_data = AddStudentInfo.query.filter_by(student_id=student_id).first()
    return render_template("student/student_dashboard.html",student_data=student_data)