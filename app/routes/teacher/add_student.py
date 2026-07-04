from flask import Blueprint,session,redirect,url_for,render_template,flash
from app.utils.add_student_form import AddStudentForm
from app.models.teacher import AddStudentInfo
from app.models.assign import Department
from app.extensions import db

add_student_bp = Blueprint(
    "add_student",
    __name__,
    url_prefix="/add_student"
)

@add_student_bp.route("/", methods=["GET", "POST"])
def add_student():

    if not session.get("teacher"):
        return redirect(url_for("login.login"))

    student_form = AddStudentForm()
    # Department dropdown load
    principal_id = session.get("temp_principal_id")
    teacher_id = session.get("teacher_id")
    departments = Department.query.filter_by(
        principal_id=principal_id,
        teacher_id=teacher_id
    ).all()

    student_form.department_id.choices = [
        (
            (d.department_id, f"{d.department_code} - {d.department_name}")
        )

        for d in departments
    ]

    if student_form.validate_on_submit():

        teacher_id = session.get("teacher_id")

        student_info = AddStudentInfo(
            student_roll=student_form.student_roll.data,
            student_full_name=student_form.student_full_name.data,
            semester=student_form.semester.data,
            group=student_form.group.data,
            department_id=student_form.department_id.data,
            teacher_id=teacher_id
        )

        db.session.add(student_info)
        db.session.commit()

        flash("Student added successfully", "success")

        return redirect(
            url_for("teacher_dashboard.teacher_dashboard")
        )

    return render_template(
        "teacher/add_student.html",
        student_form=student_form
    )