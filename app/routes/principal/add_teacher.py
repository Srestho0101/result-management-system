from flask import Blueprint,request,redirect,url_for,session,render_template,flash
from app.utils.principalForm import AddTecaherForm
from app.models.principal import TeacherAddInfo
from app.extensions import db

add_teacher_bp = Blueprint(
    "add_teacher",
    __name__,
    url_prefix="/add_teacher"
)

@add_teacher_bp.route("/",methods=["GET","POST"])
def add_teachers():

    if not session.get("principal"):
        return redirect(url_for('login.login'))
    
    add_teacher_form = AddTecaherForm()
    try:
        if add_teacher_form.validate_on_submit():
        
            teacher_data_info = TeacherAddInfo(
                teacher_id=add_teacher_form.teacher_id.data,
                first_name=add_teacher_form.first_name.data,
                last_name=add_teacher_form.last_name.data,
                institute=add_teacher_form.institute.data,
                institute_code=add_teacher_form.institute_code.data,
                phone=add_teacher_form.phone.data,
                email=add_teacher_form.email.data,
                username=add_teacher_form.username.data,
                password=add_teacher_form.password.data,
                principal_id=session["principal_id"],
                shift=session["shift"]

                )
        
            db.session.add(teacher_data_info)
            db.session.commit()

            flash("Teacher added successfully", "success")
            return redirect(url_for('principal_dashboard.principal_dashboard'))
    except Exception as e:
        db.session.rollback()
        flash(f"Somthing wrong. Maybe Teacher alrady exists","danger")
    
    return render_template(
        "principal/add_teacher.html",
        add_teacher_form=add_teacher_form,
    )







