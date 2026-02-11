from flask import Blueprint, render_template, request, redirect, session,url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from fillform import fillform


from doctor_db import doctor_registeration, doctor_valdation
from models import db, Doctor

routes = Blueprint("routes", __name__)
@routes.route("/")
def home():
    return render_template("index.html")

@routes.route("/doctorregistration", methods=["GET", "POST"])
def doctorregistration():
    if request.method == "POST":
        # Store form data temporarily in session
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
        return redirect(url_for('routes.doctorvalidation'))

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

        # Call Selenium function to verify doctor
        result = fillform(
            name=temp_doctor["name"],
            nmc_no=nmc_number,
            education=temp_doctor["degree"]
        )

        if result == "no": 
            flash("NMC number not verified. Please check and try again.") 
            return redirect(url_for("routes.doctorregistration"))
        # Save photo
        upload_folder = "static/uploads"
        os.makedirs(upload_folder, exist_ok=True)
        photo_filename = secure_filename(photo.filename)
        photo.save(os.path.join(upload_folder, photo_filename))

        # Save doctor to database
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
            nmc_number=nmc_number,
            photo=f"uploads/{photo_filename}"
        )
        db.session.add(doctor)
        db.session.commit()

        # Clear temporary session data
        session.pop("temp_doctor")
        session["doctor_phone"] = doctor.phone

        return redirect(url_for("routes.doctorpassword"))

    return render_template("doctorvalidation.html")


# ---------------- Doctor Password ----------------
@routes.route("/doctor/doctorpassword", methods=["GET", "POST"])
def doctorpassword():
    doctor_phone = session.get("doctor_phone")
    if not doctor_phone:
        return redirect(url_for("routes.doctorregistration"))

    doctor = Doctor.query.get_or_404(doctor_phone)

    if request.method == "POST":
        raw_password = request.form.get("password")
        if not raw_password or raw_password.strip() == "":
            flash("Password is required")
            return redirect(url_for("routes.doctorpassword"))

        doctor.password = generate_password_hash(raw_password)
        db.session.commit()

        # Registration completed, clear session
        session.pop("doctor_phone", None)

        return redirect(url_for("routes.home"))

    return render_template("doctorpassword.html")

@routes.route("/doctorlogin", methods=["GET", "POST"])
def doctorlogin():
    if request.method == "POST":
        phone = request.form["phone"]
        password = request.form["password"]

        user = Doctor.query.get(phone)

        if user and check_password_hash(user.password, password):
            session["doctor_phone"] = user.phone
            return redirect(url_for('routes.home'))
            # session["doctor_id"] = user.id

            # # Redirect to doctor profile
            # return redirect(url_for("routes.dr_profile1", id=user.id))
        else:
            return render_template(
                "doctorlogin.html",
                message="Invalid email or password"
            )

    return render_template("doctorlogin.html")