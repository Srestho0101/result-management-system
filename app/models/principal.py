from app.extensions import db

class TeacherAddInfo(db.Model):
    
    __tablename__ = "teacher_info"
    teacher_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    institute = db.Column(db.String(200), nullable=False)
    institute_code = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    principal_id = db.Column(
        db.Integer,
        db.ForeignKey("principal_info.principal_id"),
        nullable=False
    )
    shift = db.Column(
        db.String(20),
        nullable=False
    )
