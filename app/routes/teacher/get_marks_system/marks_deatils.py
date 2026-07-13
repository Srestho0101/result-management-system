from flask import Blueprint, render_template, redirect, url_for, session,flash
from app.models.assign import Subjects
from app.models.teacher import AddStudentInfo, MarksTopic, AddMarks

marks_details_bp = Blueprint(
    "marks_details",
    __name__,
    url_prefix="/marks_details"
)

@marks_details_bp.route("/teacher/<int:student_id>", methods=["GET","POST"])
def marks_details(student_id):
    
    if not session.get("teacher"):
        return redirect(url_for("login.login"))

    principal_id = session.get("temp_principal_id")
    student = AddStudentInfo.query.get_or_404(student_id)

    subjects = Subjects.query.filter_by(
        principal_id=principal_id
    ).all()

    marks_details = []
    for subject in subjects:
        marks = AddMarks.query.filter_by(
            student_id=student.student_id,
            subject_id=subject.subject_id
        ).all()
        marks_details.append((subject, marks))

    return render_template(
        "teacher/get_marks_system/view_details.html",
        student=student,
        marks_details=marks_details
    )