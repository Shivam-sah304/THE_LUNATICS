from flask import Blueprint, render_template, request, redirect, session,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os



from doctor_db import doctor_registeration, doctor_validation
from models import db, Doctor

routes = Blueprint("routes", __name__)
@routes.route("/")
def home():
    return render_template("index.html")

@routes.route("/doctorregistration", methods=["GET", "POST"])
def doctorregistration():
    if request.method == "GET":
        return render_template("doctorregistration.html")

    # POST logic
    name = request.form["fullname"]
    email = request.form["email"]
    phone = request.form["phone"]
    address = request.form["address"]
    dob = datetime.strptime(request.form["dob"], "%Y-%m-%d").date()
    desc = request.form.get("about")
    degree = request.form["education"]
    experience = request.form["experience"]
    specialization = request.form.get("specialization")

    doctor_registeration(name, email, phone, address, dob, desc, degree, experience, specialization)
    doctor_validation()

    return redirect(url_for("routes.doctorvalidation"))



@routes.route("/doctor/doctorvalidation",methods=["GET","POST"])
def doctorvalidation():
    doctor_id=session.get("doctor_id")
    if not doctor_id:
        return redirect(url_for("routes.doctorregistration"))
    doctor=Doctor.query.get_or_404(doctor_id)
    if request.method == "POST":
        # Get text field
        doctor.nmc_number =request.form["nmc_number"]

        # Handle file uploads
        photo = request.files.get("doctor_photo")
        nmc_photo = request.files.get("nmc_license")
        if not all([photo, nmc_photo]):
            return "All files are required", 400

        upload_folder = "static/uploads"
        os.makedirs(upload_folder, exist_ok=True)
        photo_filename = secure_filename(photo.filename)
        photo.save(os.path.join(upload_folder, photo_filename))
        doctor.photo = f"uploads/{photo_filename}"  

        license_filename = secure_filename(nmc_photo.filename)
        nmc_photo.save(os.path.join(upload_folder, license_filename))
        doctor.nmc_photo = f"uploads/{license_filename}"

        db.session.commit()
        return redirect(url_for("routes.doctorpassword"))  # go to next step

    return render_template("validation1.html")

from werkzeug.security import generate_password_hash

@routes.route("/doctor/doctorpassword", methods=["GET", "POST"])
#password
def doctorpassword():
    doctor_id = session.get("doctor_id")
    if not doctor_id:
        return redirect(url_for("routes.personal1"))  # Prevent skipping steps

    doctor = Doctor.query.get_or_404(doctor_id)

    if request.method == "POST":
        # Get password from form
        raw_password = request.form.get("password")
        if not raw_password or raw_password.strip() == "":
            return "Password is required", 400

        # Hash the password before storing
        doctor.password = generate_password_hash(raw_password)

        db.session.commit()

        # Registration completed, clear session
        session.pop("doctor_id", None)
        session["doctor_id"] = doctor_id

        return redirect(url_for('routes.home')) # Or redirect to login

    return render_template("doctorpassword.html")

@routes.route("/doctorlogin", methods=["GET", "POST"])
def doctorlogin():
    if request.method == "POST":
        phone = request.form["phone"]
        password = request.form["password"]

        user = Doctor.query.filter_by(phone=phone).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
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