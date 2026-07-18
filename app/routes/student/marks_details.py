from flask import Blueprint, render_template, session
from sqlalchemy import func

from app.routes.student.auth_check import student_roll_check
from app.models.teacher import AddMarks
from app.models.assign import Subjects
from app.extensions import db

subjects_marks_bp = Blueprint(
    "subjects_marks",
    __name__,
    url_prefix="/subjects_marks"
)


@subjects_marks_bp.route("/")
def subjects_marks():

    student_roll_check()

    student_id = session.get("student_id")

    subjects_marks = (
        db.session.query(
            Subjects.subject_id,
            Subjects.subject_code,
            Subjects.subject_name,
            func.sum(AddMarks.obtained_marks).label("total_marks")
        )
        .join(
            AddMarks,
            AddMarks.subject_id == Subjects.subject_id
        )
        .filter(
            AddMarks.student_id == student_id
        )
        .group_by(
            Subjects.subject_id,
            Subjects.subject_code,
            Subjects.subject_name
        )
        .all()
    )

    return render_template(
        "student/subjects_marks_details.html",
        subjects_marks=subjects_marks
    )