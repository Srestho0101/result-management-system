from flask import Blueprint,redirect,session,render_template,url_for
from app.models.principal import TeacherAddInfo

views_teacher_bp = Blueprint(
    "view_teachers",
    __name__,
    url_prefix="/view_teachers"
)

@views_teacher_bp.route("/")
def view_teachers():

    if not session.get("principal"):
        return redirect(url_for('login.login'))

    principal_id = session.get("principal_id")
    teachers_data = TeacherAddInfo.query.filter_by(
        principal_id=principal_id,
         shift=session["shift"]
    ).all()

    return render_template(
        "principal/view_teachers.html",
        teachers_data=teachers_data
    )