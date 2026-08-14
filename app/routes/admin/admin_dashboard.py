from flask import Blueprint, render_template, redirect, url_for, flash,session
from app.utils.form import PrincipalDataForm
from app.models.admin import PrincipalDataInfo
from app.models.teacher import AddStudentInfo
from app.models.principal import TeacherAddInfo
from app.extensions import db
from werkzeug.security import generate_password_hash

admin_bp = Blueprint("admin_dashboard",__name__,url_prefix="/admin_dashboard")
@admin_bp.route("/admin_dashboard",methods=["GET","POST"])
def admin_dashboard():

    if not session.get("admin"):
        return redirect(url_for("login.login"))
    
    principal_data_form = PrincipalDataForm()
    total_principal = PrincipalDataInfo.query.count()
    total_student = AddStudentInfo.query.count()
    total_teacher = TeacherAddInfo.query.count()

    return render_template(
        "admin/admin_dashboard.html",
        principal_data_form=principal_data_form,
        total_principal=total_principal,
        total_student=total_student,
        total_teacher=total_teacher
    )
    
@admin_bp.route("/views_principals")
def view_principals():
    if not session.get("admin"):
        return redirect(url_for("login.login"))

    principals = PrincipalDataInfo.query.all()
    
    return render_template(
        "admin/view_principals.html",
        principals = principals
    )

@admin_bp.route("/admin/<int:principal_id>")
def principal_details(principal_id):

    if not session.get("admin"):
        return redirect(url_for("login.login"))
    
    principal = PrincipalDataInfo.query.get_or_404(principal_id)

    return render_template(
        "admin/principal_details.html",
        principal=principal
    )

@admin_bp.route("/edit_and_view_principal")
def edit_and_view_principal():
    
    if not session.get("admin"):
        return redirect(url_for("login.login"))

    principals = PrincipalDataInfo.query.all()

    return render_template(
        "admin/edit_and_view_principal.html",
        principals = principals
    )

@admin_bp.route("/admin/<int:principal_id>/edit", methods=["GET", "POST"])
def edit_principal(principal_id):
    principal = PrincipalDataInfo.query.get_or_404(principal_id)
    form = PrincipalDataForm(obj=principal)

    if form.validate_on_submit():

        principal.principal_id = form.principal_id.data
        principal.first_name = form.first_name.data
        principal.last_name = form.last_name.data
        principal.mobile_number = form.mobile_number.data
        principal.email = form.email.data
        principal.institute = form.institute.data
        principal.institute_code = form.institute_code.data
        principal.username = form.username.data
        principal.password_hash = generate_password_hash(form.password.data)

        db.session.commit()

        flash("Principal information update successfully","success")

        return redirect(url_for("admin_dashboard.admin_dashboard"))
    
    return render_template(
        "admin/edit_principal.html",
        form=form
    )

@admin_bp.route("/admin/<int:principal_id>/delete",methods=["POST"])
def delete_principal(principal_id):

    principal = PrincipalDataInfo.query.get_or_404(principal_id)

    try:
        db.session.delete(principal)
        db.session.commit()
        flash("Principal Delete successfully","success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting principal: {str(e)}","danger")
    return redirect(url_for("admin_dashboard.admin_dashboard"))