from flask import session,flash,redirect,url_for

def student_roll_check():
    if not session.get("student"):
        flash("Login firts using roll number","danger")
        return redirect("home.home")