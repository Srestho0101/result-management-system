from flask import Blueprint,redirect,url_for,render_template,session,flash
from app.utils.add_student_form import AddStudentForm
from app.models.teacher import AddStudentInfo
from app.models.assign import Department,TeacherAssignment
from app.extensions import db

edit_student_bp = Blueprint(
    "edit_student",
    __name__,
    url_prefix="/edit_student"
)

@edit_student_bp.route(
    "/teacher<int:student_id>/edit",
    methods=["GET", "POST"]
)
def edit_student(student_id):

    if not session.get("teacher"):
        return redirect(url_for("login.login"))

    student_data = AddStudentInfo.query.get_or_404(student_id)

    teacher_id = session.get("teacher_id")
    principal_id = session.get("temp_principal_id")
    
    form = AddStudentForm(obj=student_data)

    assignments = TeacherAssignment.query.filter_by(
        teacher_id=teacher_id
    ).all()
    department_ids = list({
        a.department_id
        for a in assignments
    })
    departments = Department.query.filter(
        Department.principal_id == principal_id,
        Department.department_id.in_(department_ids)
    ).all()

    form.department_id.choices = [
        (
            d.department_id,
            f"{d.department_code} - {d.department_name} "
        )
        for d in departments
    ]

    if form.validate_on_submit():
        student_data.student_roll = form.student_roll.data
        student_data.student_full_name = form.student_full_name.data
        student_data.department_id = form.department_id.data
        student_data.semester = form.semester.data
        student_data.group = form.group.data

        db.session.commit()

        flash("Student Data Edited Successfully", "success")
        return redirect(url_for("show_student.show_student"))

    return render_template(
        "teacher/edit_student.html",
        form=form,
        student_data=student_data
    )

@edit_student_bp.route("/teacher/<int:student_id>/delete", methods=["GET","POST"])
def delete_student(student_id):

    if not session.get("teacher"):
        return redirect(url_for("login.login"))

    student = AddStudentInfo.query.get_or_404(student_id)

    try:
        db.session.delete(student)
        db.session.commit()
        flash("Student Deleted Successfully", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error Deleting Student: {e}", "danger")

    return redirect(url_for("show_student.show_student"))