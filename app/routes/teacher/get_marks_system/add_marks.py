from flask import Blueprint, render_template, redirect, url_for, session, flash
from app.models.assign import Subjects
from app.models.teacher import (
    AddStudentInfo,
    MarksTopic,
    AddMarks
)
from app.utils.add_marks_form import AddMarksForm
from app.extensions import db

add_marks_bp = Blueprint(
    "add_marks",
    __name__,
    url_prefix="/add_marks"
)

@add_marks_bp.route("/teacher/<int:student_id>", methods=["GET", "POST"])
def add_marks(student_id):

    if not session.get("teacher"):
        return redirect(url_for("login.login"))

    teacher_id = session.get("teacher_id")
    principal_id = session.get("temp_principal_id")
    student = AddStudentInfo.query.get_or_404(student_id)

    form = AddMarksForm()

    subjects = Subjects.query.filter_by(
        principal_id=principal_id
    ).all()

    form.subject.choices = [
        (
            s.subject_id,
            f"{s.subject_code} - {s.subject_name}"
        )
        for s in subjects
    ]

    topics = MarksTopic.query.filter_by(
        teacher_id=teacher_id
    ).all()

    form.mart_topic.choices = [
        (
            t.marks_topic_id,
            f"{t.marks_topic_name} ({t.full_marks})"
        )
        for t in topics
    ]

    if form.validate_on_submit():

        existing = AddMarks.query.filter_by(
            student_id=student.student_id,
            subject_id=form.subject.data,
            marks_topic_id=form.mart_topic.data
        ).first()

        if existing:
            flash(
                "Marks already exists.",
                "warning"
            )
            return redirect(
                url_for(
                    "add_marks.add_marks",
                    student_id=student.student_id
                )
            )

        mark = AddMarks(
            student_id=student.student_id,
            subject_id=form.subject.data,
            teacher_id=teacher_id,
            marks_topic_id=form.mart_topic.data,
            obtained_marks=form.get_marks.data
        )

        db.session.add(mark)
        db.session.commit()

        flash(
            "Marks Added Successfully",
            "success"
        )

        return redirect(
            url_for("get_marks.show_student")
        )

    return render_template(
        "teacher/get_marks_system/add_marks.html",
        form=form,
        student=student
    )