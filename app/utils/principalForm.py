from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Regexp,EqualTo

class AddTeacherForm(FlaskForm):
    teacher_id = IntegerField(
        "Teacher ID",
        validators=[
            DataRequired()
            ]
        )
    
    first_name = StringField(
        "Enter First name",
        validators=[
            DataRequired(),
            Length(min=2,max=50)
        ]
    )
    last_name = StringField(
        "Enter last name",
        validators=[
            DataRequired(),
            Length(min=2,max=50)
        ]
    )
    institute = StringField(
        "Enter Institute name",
        validators=[
            DataRequired(),
            Length(min=5,max=200)
        ]
    )
    institute_code = StringField(
        "Enter Institute Code",
        validators=[
             DataRequired(),
             Length(min=3,max=20)
        ]
    )
    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Length(min=11, max=11),
            Regexp(r'^\d{11}$')
        ]
    )
    email = StringField(
        "Enter email ",
        validators=[
            DataRequired(),
            Length(min=1,max=50)
        ]
    )

    username = StringField(
        "Enter username",
        validators=[
            DataRequired(),
            Length(min=6,max=120)
        ]
    )
    
    password = PasswordField(
        "Enter a Strong Password",
        validators=[
            DataRequired(),
            Length(min=6, max=32)
        ]
    )

    retype_password = PasswordField(
        "Retype password",
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )

    submit = SubmitField("Add Principal")

