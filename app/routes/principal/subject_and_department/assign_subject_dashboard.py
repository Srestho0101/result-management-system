from flask import Blueprint,redirect,render_template,session,url_for,flash
from app.models.assign import Subjects,Department
from app.utils.assign_form import SubjectForm,DepartmentForm
from app.extensions import db

assign_subject_dashboard_bp = Blueprint(
    "assign_subject_dashboard",
    __name__,
    url_prefix="/assign_subject_dashboard"
)

@assign_subject_dashboard_bp.route("assign_subject_dashboard")
def assign_subject_dashboard():
       
    if not session.get("principal"):
        return redirect(url_for("login.login"))
    
    principal_id = session.get("principal_id")
    total_department = Department.query.filter_by(
        principal_id=principal_id
    ).count()

    total_subject = Subjects.query.filter_by(
        principal_id=principal_id
    ).count()

    return render_template(
        "principal/subject_and_department/assign_subject_dashboard.html",
        total_department = total_department,
        total_subject = total_subject
    )

@assign_subject_dashboard_bp.route("/subject/<int:subject_id>/edit",methods=["GET","POST"])
def edit_subject(subject_id):
    if not session.get("principal_id"):
        return redirect(url_for("login.login"))

    subject = Subjects.query.get_or_404(subject_id)
    form =  SubjectForm(obj=subject)  

    if form.validate_on_submit():
        subject.subject_code = form.subject_code.data
        subject.subject_name = form.subject_name.data

        db.session.commit()
        flash("Subject eddited successfully","success")

        return redirect(url_for("show_subjects.show_subjects"))

    return render_template(
        "principal/subject_and_department/edit_subject.html",
        form = form,
        subject = subject
    )

@assign_subject_dashboard_bp.route("/department/<int:department_id>/edit",methods=["GET","POST"])
def edit_department(department_id):
    if not session.get("principal_id"):
        return redirect(url_for("login.login"))

    department = Department.query.get_or_404(department_id)
    form =  DepartmentForm(obj=department)  

    if form.validate_on_submit():
        department.department_code = form.department_code.data
        department.department_name = form.department_name.data

        db.session.commit()
        flash("Department eddited successfully","success")

        return redirect(url_for("show_subjects.show_department"))

    return render_template(
        "principal/subject_and_department/edit_department.html",
        form = form,
        department=department
    )


@assign_subject_dashboard_bp.route("/subject/<int:subject_id>/delete", methods=["POST"])
def delete_subject(subject_id):
    subject= Subjects.query.get_or_404(subject_id)

    try:
        db.session.delete(subject)   
        db.session.commit()
        flash("Subject deleted successfully", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting subject: {str(e)}", "danger")

    return redirect(url_for('assign_subject_dashboard.assign_subject_dashboard'))


@assign_subject_dashboard_bp.route("/department/<int:department_id>/delete", methods=["POST"])
def delete_department(department_id):
    department= Department.query.get_or_404(department_id)

    try:
        db.session.delete(department)   
        db.session.commit()
        flash("Subject deleted successfully", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting department: {str(e)}", "danger")

    return redirect(url_for('assign_subject_dashboard.assign_subject_dashboard'))