from flask import Blueprint, render_template, session, request
from sqlalchemy import func

from app.routes.student.auth_check import student_roll_check
from app.models.teacher import Attendance
from app.extensions import db

student_attendance_bp = Blueprint(
    "student_attendance",
    __name__,
    url_prefix="/student_attendance"
)


@student_attendance_bp.route("/")
def attendance():
    student_roll_check()
    student_id = session.get("student_id")
    page = request.args.get("page", 1, type=int)
    attendance = (
        Attendance.query
        .filter_by(student_id=student_id)
        .order_by(Attendance.attendance_date.desc())
        .paginate(page=page, per_page=15)
    )

    total_class = (
        db.session.query(func.count(Attendance.attendance_id))
        .filter_by(student_id=student_id)
        .scalar()
    ) or 0

    total_present = (
        db.session.query(func.count(Attendance.attendance_id))
        .filter_by(
            student_id=student_id,
            status="P"
        )
        .scalar()
    ) or 0

    total_absent = (
        db.session.query(func.count(Attendance.attendance_id))
        .filter_by(
            student_id=student_id,
            status="A"
        )
        .scalar()
    ) or 0

    percentage = 0
    if total_class > 0:
        percentage = round((total_present / total_class) * 100, 2)

    return render_template(
        "student/attendance.html",
        attendance=attendance,
        total_class=total_class,
        total_present=total_present,
        total_absent=total_absent,
        percentage=percentage
    )