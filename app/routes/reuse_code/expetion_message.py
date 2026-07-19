from flask import session,flash
from app.extensions import db

def error_message():
    db.session.rollback()
    flash("Somthing Wrong","danger")