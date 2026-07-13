from app.extensions import db
from datetime import datetime


# ==========================
# Department
# ==========================
class Department(db.Model):
    __tablename__ = "departments"

    department_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    department_code = db.Column(
        db.Integer,
        nullable=False
    )

    department_name = db.Column(
        db.String(150),
        nullable=False
    )

    principal_id = db.Column(
        db.Integer,
        db.ForeignKey("principal_info.principal_id"),
        nullable=False
    )


    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("teacher_info.teacher_id")
    )
    __table_args__ = (
        db.UniqueConstraint(
            "principal_id",
            "department_code",
            name="unique_department_per_principal"
        ),
    )


# ==========================
# Subjects
# ==========================
class Subjects(db.Model):
    __tablename__ = "subjects"

    subject_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    subject_code = db.Column(
        db.String(20),
        nullable=False
    )

    subject_name = db.Column(
        db.String(150),
        nullable=False
    )

    principal_id = db.Column(
        db.Integer,
        db.ForeignKey("principal_info.principal_id"),
        nullable=False
    )

    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("teacher_info.teacher_id")
    )
    __table_args__ = (
        db.UniqueConstraint(
            "principal_id",
            "subject_code",
            name="unique_subject_per_principal"
        ),
    )


# ==========================
# Curriculum
# Department + Semester + Subject
# ==========================
class Curriculum(db.Model):

    __tablename__ = "curriculum"

    curriculum_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.department_id"),
        nullable=False
    )

    semester = db.Column(
        db.Integer,
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.subject_id"),
        nullable=False
    )

    subject = db.relationship(
        "Subjects",
        lazy=True
    )

    department = db.relationship(
        "Department",
        lazy=True
    )


# ==========================
# Teacher Assignment
# ==========================
class TeacherAssignment(db.Model):

    __tablename__ = "teacher_assignments"

    assignment_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("teacher_info.teacher_id"),
        nullable=False
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.department_id"),
        nullable=False
    )

    semester = db.Column(
        db.Integer,
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.subject_id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    teacher = db.relationship(
        "TeacherAddInfo",
        lazy=True
    )

    department = db.relationship(
        "Department",
        lazy=True
    )

    subject = db.relationship(
        "Subjects",
        lazy=True
    )