from flask import Blueprint,redirect,url_for,flash,render_template,session
from app.models.teacher import AddStudentInfo

view_student_details_bp = Blueprint(
    "view_student_details",
    __name__,
    url_prefix="/view_student_details"
)
@view_student_details_bp.route("/teacher<int:student_id>")
def view_student_details(student_id):
    if not session.get("teacher"):
        return redirect(url_for("login.login"))
    student = AddStudentInfo.query.get_or_404(student_id)

    return render_template(
        "teacher/get_marks_system/view_details.html",
        student=student
    )