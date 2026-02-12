from flask import Blueprint, render_template, request, redirect, session,url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from fillform import fillform
from functools import wraps

from models import db, Doctor,Patient

routes = Blueprint("routes", __name__)


@routes.route("/")
def home():
    return render_template("index.html")


@routes.route("/doctorregistration", methods=["GET", "POST"])
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

    # ✅ Pass temp_doctor to template
    return render_template("doctorvalidation.html", temp_doctor=temp_doctor)

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
        # session.pop("temp_doctor", None)
        # # session["doctor_phone"] = doctor_p
        session.pop("doctor_phone", None)
        session["doctor_phone"] = doctor.phone 

        flash("Registration completed successfully!")
        return redirect(url_for("routes.profileseenbydoctor"))

    return render_template("doctorpassword.html")




def doctor_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "doctor_phone" not in session:
            return redirect(url_for("routes.doctorlogin"))
        return f(*args, **kwargs)
    return decorated_function



@routes.route('/profileseenbydoctor', methods=['GET', 'POST'])
@doctor_login_required
def profileseenbydoctor():
    # Debug: print session contents
    print("Session data:", session)

    # Get the doctor's phone from session
    doctor_phone = session.get("doctor_phone")
    if not doctor_phone:
        # If no session, redirect to login
        flash("Please log in first.")
        return redirect(url_for('routes.doctorlogin'))

    # Query the doctor using phone (primary key)
    doctor = Doctor.query.filter_by(phone=doctor_phone).first()
    if not doctor:
        # If doctor not found in DB
        flash("Doctor not found in the database.")
        return redirect(url_for('routes.doctorlogin'))

    # Pass the doctor object to template
    return render_template('profileseenbydoctor.html', doctor=doctor)



@routes.route('/doctorlogin', methods=["POST", "GET"])
def doctorlogin():
    if request.method == "POST":
        phone = request.form.get('phone')
        password = request.form.get('password')

        user = Doctor.query.filter_by(phone=phone).first()
        if not user:
            flash("User not found")
            return redirect(url_for('routes.doctorlogin'))

        if not check_password_hash(user.password, password):
            flash("Invalid phone or password")
            return redirect(url_for('routes.doctorlogin'))

        # ✅ Set session correctly BEFORE redirect
        session["doctor_phone"] = user.phone

        return redirect(url_for('routes.profileseenbydoctor'))

    return render_template("doctorlogin.html")



@routes.route("/patient/patient_register", methods=["GET", "POST"])
def patient_register():
    if request.method == "POST":
        patient = Patient(
            name=request.form["full_name"],
            phone=request.form["phone"],
            email=request.form["email"],
            desc=request.form["problem"],
            tem_address=request.form["temporary_address"],
            per_address=request.form["permanent_address"]
        )
        db.session.add(patient)
        db.session.commit()  # assign patient.id but do not commit 
        session["patient_id"] = patient.id
        return redirect(url_for("routes.patient_contact"))

    return render_template("patient_register.html")


# Step 2: Contact person
@routes.route("/patient/patient_contact", methods=["GET", "POST"])
def patient_contact():
    patient_id = session.get("patient_id")
    if not patient_id:
        return redirect(url_for("routes.patient_register"))

    patient = Patient.query.get_or_404(patient_id)

    if request.method == "POST":
        patient.num1 = request.form["contact1_phone"]
        patient.closed_person1 = request.form["contact1_name"]
        patient.relation1 = request.form["contact1_relation"]
        patient.num2 = request.form["contact2_phone"]
        patient.closed_person2 = request.form["contact2_name"]
        patient.relation2 = request.form["contact2_relation"]
        patient.num3 = request.form["contact3_phone"]
        patient.relation3 = request.form["contact3_relation"]
        patient.closed_person3 = request.form["contact3_name"]

        db.session.commit()
        return redirect(url_for("routes.patient_password"))

    return render_template("patient_contact.html")


# Step 3: Set password
@routes.route("/patient/patient_password", methods=["GET", "POST"])
def patient_password():
    patient_id = session.get("patient_id")
    if not patient_id:
        return redirect(url_for("routes.patient_register"))

    patient = Patient.query.get_or_404(patient_id)

    if request.method == "POST":
        raw_password = request.form.get("password")
        if not raw_password or raw_password.strip() == "":
            return "Password is required", 400

        # Hash the password and save
        patient.password = generate_password_hash(raw_password)
        db.session.commit()

        # Clear session
        session.pop("patient_id", None)

        return redirect(url_for("routes.home"))

    return render_template("patient_password.html")



@routes.route("/patientlogin", methods=["GET", "POST"])
def patientlogin():
    if request.method == "POST":
        phone = request.form["phone"]
        password = request.form["password"]

        user = Patient.query.filter_by(phone=phone).first()

        if user and check_password_hash(user.password, password):
            session["user_phone"] = user.phone
            return redirect("/doctor_table")
        else:
            return render_template(
                "patientlogin.html",
                message="Invalid email or password"
            )

    return render_template("patientlogin.html")

def user_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_phone" not in session:
            return redirect(url_for("routes.patientlogin"))  # redirect to login if not logged in
        return f(*args, **kwargs)
    return decorated_function

# @routes.route('/get_id')
# @user_login_required
# @doctor_login_required
# def get_id():
#     doctor_phone = session.get('doctor_phone')
#     user_phone = session.get('user_phone')
#     print(doctor_phone, user_phone)
#     return render_template('chats.html')







@routes.route("/doctor_table")
@user_login_required
def doctor_table():
    doctors = Doctor.query.all()

    return render_template("doctor_table.html", doctors=doctors)



@routes.route("/doctor_patient/<phone>")
@user_login_required
def doctor_patient(phone):
    print(phone)
    doctor = Doctor.query.get_or_404(phone)
    doctor = {
    "photo": "uploads/abc.jpg",
    "name": "Dr. Rajan",
    "status": 1,

    "id": 123,
    "rating": 4,
    "specialty": "Cardiology",
    "about": "Experienced cardiologist ...",
    "facebook": "https://facebook.com/rajan",
    "whatsapp": "919876543210"
    }

    print(phone)  # works because phone is PK
    return render_template("doctor_patient.html", doctor=doctor) 
    








@routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.doctorlogin'))