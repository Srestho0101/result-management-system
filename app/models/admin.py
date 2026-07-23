from app.extensions import db
class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.String(120), nullable=False)

class PrincipalDataInfo(db.Model):
    __tablename__ = "principal_info"

    principal_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    institute = db.Column(db.String(200),nullable=False,unique=True)
    institute_code = db.Column(db.String(30),nullable=False,unique=True)
    username = db.Column(db.String(120),nullable=False,unique=True)
    password = db.Column(db.String(120), nullable=False)
    