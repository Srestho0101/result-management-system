from flask import Blueprint,redirect,url_for,render_template,request

student_dashboard_bp = Blueprint(
    "student_dashboard",
    __name__,
    url_prefix="/student_dashboard"
)

student_dashboard_bp.route("/")
def student_dashboard():
    render_template("student/student_dashboard.html")