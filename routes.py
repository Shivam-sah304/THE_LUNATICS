from flask import Blueprint, render_template, request, redirect, session,url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from fillform import fillform
from functools import wraps

from models import db, Doctor

routes = Blueprint("routes", __name__)
@routes.route("/")
def home():
    return render_template("index.html")

@routes.route("/doctor/doctorregistration", methods=["GET", "POST"])
def doctorregistration():
    if request.method == "POST":
        session["temp_doctor"] = {
            "name": request.form["fullname"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "address": request.form["address"],
            "dob": request.form["dob"],
            "desc": request.form.get("about", ""),
            "degree": request.form["education"],
            "experience": request.form["experience"],
            "specialization": request.form.get("specialization", "")
        }

        return redirect(url_for("routes.doctorvalidation"))

    return render_template("doctorregistration.html")

# ---------------- Doctor Validation ----------------
@routes.route("/doctor/doctorvalidation", methods=["GET", "POST"])
def doctorvalidation():
    temp_doctor = session.get("temp_doctor")

    if not temp_doctor:
        return redirect(url_for("routes.doctorregistration"))

    if request.method == "POST":
        nmc_number = request.form.get("nmc_number")
        photo = request.files.get("doctor_photo")

        if not nmc_number or not photo:
            flash("All fields are required")
            return redirect(url_for("routes.doctorvalidation"))

        # Verify using Selenium
        result = fillform(
            name=temp_doctor["name"],
            nmc_no=nmc_number,
            education=temp_doctor["degree"]
        )

        if result == "no":
            flash("You are not a verified doctor")
            session.pop("temp_doctor", None)
            return redirect(url_for("routes.doctorregistration"))

        # Save photo temporarily
        upload_folder = "static/uploads"
        os.makedirs(upload_folder, exist_ok=True)
        photo_filename = secure_filename(photo.filename)
        photo_path = os.path.join(upload_folder, photo_filename)
        photo.save(photo_path)

        # Store extra validation data temporarily
        temp_doctor["nmc_number"] = nmc_number
        temp_doctor["photo"] = f"uploads/{photo_filename}"

        session["temp_doctor"] = temp_doctor

        return redirect(url_for("routes.doctorpassword"))

    return render_template("doctorvalidation.html")

# ---------------- Doctor Password ----------------
@routes.route("/doctor/doctorpassword", methods=["GET", "POST"])
def doctorpassword():
    temp_doctor = session.get("temp_doctor")
    
    if not temp_doctor:
        return redirect(url_for("routes.doctorregistration"))

    if request.method == "POST":
        raw_password = request.form.get("password")

        if not raw_password or raw_password.strip() == "":
            flash("Password is required")
            return redirect(url_for("routes.doctorpassword"))

        # Create doctor object NOW (only here)
        doctor = Doctor(
            name=temp_doctor["name"],
            email=temp_doctor["email"],
            phone=temp_doctor["phone"],
            address=temp_doctor["address"],
            dob=datetime.strptime(temp_doctor["dob"], "%Y-%m-%d").date(),
            desc=temp_doctor["desc"],
            degree=temp_doctor["degree"],
            experience=temp_doctor["experience"],
            specialization=temp_doctor["specialization"],
            nmc_number=temp_doctor["nmc_number"],
            photo=temp_doctor["photo"],
            password=generate_password_hash(raw_password)
        )

        db.session.add(doctor)
        db.session.commit()

        # Clear session completely
        session.pop("temp_doctor", None)

        flash("Registration completed successfully!")
        return redirect(url_for("routes.home"))

    return render_template("doctorpassword.html")


# @routes.route("/doctorlogin", methods=["GET", "POST"])
# def doctorlogin():
#     if request.method == "POST":
#         phone = request.form["phone"]
#         password = request.form["password"]

#         user = Doctor.query.get(phone)

#         if user and check_password_hash(user.password, password):
#             session["doctor_phone"] = user.phone
#             return redirect(url_for('routes.home'))
#             # session["doctor_id"] = user.id

#             # # Redirect to doctor profile
#             # return redirect(url_for("routes.dr_profile1", id=user.id))
#         else:
#             return render_template(
#                 "doctorlogin.html",
#                 message="Invalid email or password"
#             )

#     return render_template("doctorlogin.html")


@routes.route('/doctorlogin', methods=["POST","GET"])
def doctorlogin():
    if request.method=="POST":
        phone = request.form.get('phone')
        password = request.form.get('password')

        user = Doctor.query.filter_by(phone=phone).first()
        if user == None:
            return 'Cant login'
       
        if check_password_hash(user.password, password):
            session["user_id"] = user.phone
            return redirect(url_for('routes.home'))
        else:
            return "Invalid phone or password"  
    return render_template("doctorlogin.html")
    



# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if "user_id" not in session:
#             return redirect(url_for("routes.doctorvalidation"))  # redirect to login if not logged in
#         return f(*args, **kwargs)
#     return decorated_function
