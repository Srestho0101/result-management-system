import re
import pdfplumber
from flask import render_template, flash, redirect, url_for,Blueprint,session
from app.extensions import db
from app.models.teacher import AddStudentInfo
from app.utils.cgpa_form import UploadCGPAForm

upload_cgpa_bp = Blueprint(
    "upload_cgpa",
    __name__,
    url_prefix="/upload_cgpa"
)

@upload_cgpa_bp.route("/", methods=["GET", "POST"])
def upload_cgpa():
    if not session.get("admin"):
        return redirect(url_for("login.login"))
    
    form = UploadCGPAForm()
    if form.validate_on_submit():
        pdf = form.pdf.data
        updated = 0
        not_found = 0
        students = {
            student.student_roll: student
            for student in AddStudentInfo.query.all()
        }
        pattern = re.compile(r"(\d+)\s*\((\d+\.\d+)\)")
        with pdfplumber.open(pdf) as pdf_file:
            for page in pdf_file.pages:
                text = page.extract_text()
                if not text:
                    continue
                matches = pattern.findall(text)
                for roll, cgpa in matches:
                    roll = int(roll)
                    cgpa = float(cgpa)
                    student = students.get(roll)
                    if student:
                        student.cgpa = cgpa
                        updated += 1
                    else:
                        not_found += 1

        db.session.commit()
        flash(f"Updated : {updated} | Not Found : {not_found}","success")
        return redirect(url_for("admin_dashboard.admin_dashboard"))

    return render_template(
        "admin/upload_cgpa.html",
        form=form
    )