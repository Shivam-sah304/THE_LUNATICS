# from flask import Blueprint, render_template, request, redirect, session,url_for,flash
# from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.utils import secure_filename
# from datetime import datetime
# import os
# from fillform import fillform
# from functools import wraps

# from models import db, Doctor,Patient

# routes = Blueprint("routes", __name__)
# @routes.route("/")
# def home():
#     return render_template("index.html")

# @routes.route("/doctor/doctorregistration", methods=["GET", "POST"])
# def doctorregistration():
#     if request.method == "POST":
#         session["temp_doctor"] = {
#             "name": request.form["fullname"],
#             "email": request.form["email"],
#             "phone": request.form["phone"],
#             "address": request.form["address"],
#             "dob": request.form["dob"],
#             "desc": request.form.get("about", ""),
#             "degree": request.form["education"],
#             "experience": request.form["experience"],
#             "specialization": request.form.get("specialization", "")
#         }

#         return redirect(url_for("routes.doctorvalidation"))

#     return render_template("doctorregistration.html")

# # ---------------- Doctor Validation ----------------
# @routes.route("/doctor/doctorvalidation", methods=["GET", "POST"])
# def doctorvalidation():
#     temp_doctor = session.get("temp_doctor")

#     if not temp_doctor:
#         return redirect(url_for("routes.doctorregistration"))

#     if request.method == "POST":
#         nmc_number = request.form.get("nmc_number")
#         photo = request.files.get("doctor_photo")

#         if not nmc_number or not photo:
#             flash("All fields are required")
#             return redirect(url_for("routes.doctorvalidation"))

#         # Verify using Selenium
#         result = fillform(
#             name=temp_doctor["name"],
#             nmc_no=nmc_number,
#             education=temp_doctor["degree"]
#         )

#         if result == "no":
#             flash("You are not a verified doctor")
#             session.pop("temp_doctor", None)
#             return redirect(url_for("routes.doctorregistration"))

#         # Save photo temporarily
#         upload_folder = "static/uploads"
#         os.makedirs(upload_folder, exist_ok=True)
#         photo_filename = secure_filename(photo.filename)
#         photo_path = os.path.join(upload_folder, photo_filename)
#         photo.save(photo_path)

#         # Store extra validation data temporarily
#         temp_doctor["nmc_number"] = nmc_number
#         temp_doctor["photo"] = f"uploads/{photo_filename}"

#         session["temp_doctor"] = temp_doctor

#         return redirect(url_for("routes.doctorpassword"))

#     # ✅ Pass temp_doctor to template
#     return render_template("doctorvalidation.html", temp_doctor=temp_doctor)

# # ---------------- Doctor Password ----------------
# @routes.route("/doctor/doctorpassword", methods=["GET", "POST"])
# def doctorpassword():
#     temp_doctor = session.get("temp_doctor")
    
#     if not temp_doctor:
#         return redirect(url_for("routes.doctorregistration"))

#     if request.method == "POST":
#         raw_password = request.form.get("password")

#         if not raw_password or raw_password.strip() == "":
#             flash("Password is required")
#             return redirect(url_for("routes.doctorpassword"))

#         # Create doctor object NOW (only here)
#         doctor = Doctor(
#             name=temp_doctor["name"],
#             email=temp_doctor["email"],
#             phone=temp_doctor["phone"],
#             address=temp_doctor["address"],
#             dob=datetime.strptime(temp_doctor["dob"], "%Y-%m-%d").date(),
#             desc=temp_doctor["desc"],
#             degree=temp_doctor["degree"],
#             experience=temp_doctor["experience"],
#             specialization=temp_doctor["specialization"],
#             nmc_number=temp_doctor["nmc_number"],
#             photo=temp_doctor["photo"],
#             password=generate_password_hash(raw_password)
#         )

#         db.session.add(doctor)
#         db.session.commit()

#         # Clear session completely
#         # session.pop("temp_doctor", None)
#         # # session["doctor_phone"] = doctor_p
#         session.pop("doctor_phone", None)
#         session["doctor_phone"] = doctor.phone 

#         flash("Registration completed successfully!")
#         return redirect(url_for("routes.profileseenbydoctor"))

#     return render_template("doctorpassword.html")


# # @routes.route("/doctorlogin", methods=["GET", "POST"])
# # def doctorlogin():
# #     if request.method == "POST":
# #         phone = request.form["phone"]
# #         password = request.form["password"]

# #         user = Doctor.query.get(phone)

# #         if user and check_password_hash(user.password, password):
# #             session["doctor_phone"] = user.phone
# #             return redirect(url_for('routes.home'))
# #             # session["doctor_id"] = user.id

# #             # # Redirect to doctor profile
# #             # return redirect(url_for("routes.dr_profile1", id=user.id))
# #         else:
# #             return render_template(
# #                 "doctorlogin.html",
# #                 message="Invalid email or password"
# #             )

# #     return render_template("doctorlogin.html")


# @routes.route('/profileseenbydoctor', methods=['GET', 'POST'])
# def profileseenbydoctor():
#     # Debug: print session contents
#     print("Session data:", session)

#     # Get the doctor's phone from session
#     doctor_phone = session.get("doctor_phone")
#     if not doctor_phone:
#         # If no session, redirect to login
#         flash("Please log in first.")
#         return redirect(url_for('routes.doctorlogin'))

#     # Query the doctor using phone (primary key)
#     doctor = Doctor.query.filter_by(phone=doctor_phone).first()
#     if not doctor:
#         # If doctor not found in DB
#         flash("Doctor not found in the database.")
#         return redirect(url_for('routes.doctorlogin'))

#     # Pass the doctor object to template
#     return render_template('profileseenbydoctor.html', doctor=doctor)





# @routes.route('/doctorlogin', methods=["POST", "GET"])
# def doctorlogin():
#     if request.method == "POST":
#         phone = request.form.get('phone')
#         password = request.form.get('password')

#         user = Doctor.query.filter_by(phone=phone).first()
#         if not user:
#             flash("User not found")
#             return redirect(url_for('routes.doctorlogin'))

#         if not check_password_hash(user.password, password):
#             flash("Invalid phone or password")
#             return redirect(url_for('routes.doctorlogin'))

#         # ✅ Set session correctly BEFORE redirect
#         session["doctor_phone"] = user.phone

#         return redirect(url_for('routes.profileseenbydoctor'))

#     return render_template("doctorlogin.html")

# # def login_required(f):
# #     @wraps(f)
# #     def decorated_function(*args, **kwargs):
# #         if "user_id" not in session:
# #             return redirect(url_for("routes.doctorvalidation"))  # redirect to login if not logged in
# #         return f(*args, **kwargs)
# #     return decorated_function
# #prersonal
# # Step 1: Register patient

# @routes.route("/patient/patient_register", methods=["GET", "POST"])
# def patient_register():
#     if request.method == "POST":
#         patient = Patient(
#             name=request.form["full_name"],
#             phone=request.form["phone"],
#             email=request.form["email"],
#             desc=request.form["problem"],
#             tem_address=request.form["temporary_address"],
#             per_address=request.form["permanent_address"]
#         )
#         db.session.add(patient)
#         db.session.commit()  # assign patient.id but do not commit 
#         session["patient_id"] = patient.id
#         return redirect(url_for("routes.patient_contact"))

#     return render_template("patient_register.html")


# # Step 2: Contact person
# @routes.route("/patient/patient_contact", methods=["GET", "POST"])
# def patient_contact():
#     patient_id = session.get("patient_id")
#     if not patient_id:
#         return redirect(url_for("routes.patient_register"))

#     patient = Patient.query.get_or_404(patient_id)

#     if request.method == "POST":
#         patient.num1 = request.form["contact1_phone"]
#         patient.closed_person1 = request.form["contact1_name"]
#         patient.relation1 = request.form["contact1_relation"]
#         patient.num2 = request.form["contact2_phone"]
#         patient.closed_person2 = request.form["contact2_name"]
#         patient.relation2 = request.form["contact2_relation"]
#         patient.num3 = request.form["contact3_phone"]
#         patient.relation3 = request.form["contact3_relation"]
#         patient.closed_person3 = request.form["contact3_name"]

#         db.session.commit()
#         return redirect(url_for("routes.patient_password"))

#     return render_template("patient_contact.html")


# # Step 3: Set password
# @routes.route("/patient/patient_password", methods=["GET", "POST"])
# def patient_password():
#     patient_id = session.get("patient_id")
#     if not patient_id:
#         return redirect(url_for("routes.patient_register"))

#     patient = Patient.query.get_or_404(patient_id)

#     if request.method == "POST":
#         raw_password = request.form.get("password")
#         if not raw_password or raw_password.strip() == "":
#             return "Password is required", 400

#         # Hash the password and save
#         patient.password = generate_password_hash(raw_password)
#         db.session.commit()

#         # Clear session
#         session.pop("patient_id", None)

#         return redirect(url_for("routes.doctor_table"))

#     return render_template("patient_password.html")
# @routes.route("/patientlogin", methods=["GET", "POST"])

# def patientlogin():
#     if request.method == "POST":
#         phone = request.form["phone"]
#         password = request.form["password"]

#         user = Patient.query.filter_by(phone=phone).first()

#         if user and check_password_hash(user.password, password):
#             session["user_id"] = user.id
#             return redirect("/doctor_table")
#         else:
#             return render_template(
#                 "patientlogin.html",
#                 message="Invalid email or password"
#             )

#     return render_template("patientlogin.html")


# @routes.route("/doctor_table")
# def doctor_table():
#     doctors = Doctor.query.all()
#     return render_template("doctor_table.html", doctors=doctors)
# @routes.route("/doctor/<phone>")
# def doctor_patient(phone):
#     doctor = Doctor.query.get_or_404(phone)  # works because phone is PK
#     return render_template("doctor_patient.html", doctor=doctor) 



# #delete account
# @routes.route("/delete_account", methods=["POST"])
# def delete_account():
#     doctor_phone = session.get("doctor_phone")
#     doctor = Doctor.query.get_or_404(doctor_phone)

#     db.session.delete(doctor)
#     db.session.commit()
#     session.pop("doctor_phone", None)  # log out user
#     flash("Your account has been deleted.")
#     return redirect(url_for("routes.home"))
# #edit account
# @routes.route("/edit_profile", methods=["GET", "POST"])
# def edit_profile():
#     doctor_phone = session.get("doctor_phone")  # or however you store logged-in user
#     doctor = Doctor.query.get_or_404(doctor_phone)

#     if request.method == "POST":
#         doctor.name = request.form.get("name")
#         doctor.specialization = request.form.get("specialization")
#         doctor.facebook = request.form.get("facebook")
#         doctor.desc = request.form.get("desc")
#         # Add other fields if needed
#         db.session.commit()
#         flash("Profile updated successfully.")
#         return redirect(url_for("routes.profileseenbydoctor", phone=doctor.phone))

#     return render_template("edit_profile.html", doctor=doctor)
# #change password
# from werkzeug.security import generate_password_hash, check_password_hash

# @routes.route("/change_password", methods=["GET", "POST"])
# def change_password():
#     doctor_phone = session.get("doctor_phone")
#     doctor = Doctor.query.get_or_404(doctor_phone)

#     if request.method == "POST":
#         old_password = request.form.get("old_password")
#         new_password = request.form.get("new_password")
#         confirm_password = request.form.get("confirm_password")

#         if not check_password_hash(doctor.password, old_password):
#             flash("Old password is incorrect")
#             return redirect(url_for("routes.change_password"))

#         if new_password != confirm_password:
#             flash("Passwords do not match")
#             return redirect(url_for("routes.change_password"))

#         doctor.password = generate_password_hash(new_password)
#         db.session.commit()
#         flash("Password changed successfully")
#         return redirect(url_for("routes.doctor_patient", phone=doctor.phone))

#     return render_template("change_password.html")



# ------

from flask import Blueprint, render_template, request, redirect, session,url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from fillform import fillform
from functools import wraps

from models import db, Doctor,Patient,Rating,Report

routes = Blueprint("routes", __name__)


@routes.route("/")
def home():
    return render_template("home.html")


#endoet
@routes.route('/index')
def index():
    return render_template('index.html')

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

    
    return render_template("doctorvalidation.html", temp_doctor=temp_doctor)


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

        
        session.pop("doctor_phone", None)
        session["doctor_phone"] = doctor.phone 

        flash("Registration completed successfully!")
        return redirect(url_for("routes.doctorlogin"))

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

        #  Set session correctly BEFORE redirect
        session["doctor_phone"] = user.phone
        session['role'] = 'doctor'
        

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

        return redirect(url_for("routes.patientlogin"))

    return render_template("patient_password.html")
@routes.route("/patientlogin", methods=["GET", "POST"])
def patientlogin():
    if request.method == "POST":
        phone = request.form["phone"]
        password = request.form["password"]

        user = Patient.query.filter_by(phone=phone).first()

        if user and check_password_hash(user.password, password):
            session.permanent = True  # Make session permanent
            session["user_phone"] = user.phone
            session['role'] = 'patient'
            return redirect(url_for("routes.doctor_table", user_id=user.phone))
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


@routes.route("/doctor_table")
@user_login_required
def doctor_table():
    doctors = Doctor.query.all()

    return render_template("doctor_table.html", doctors=doctors)

@routes.route("/patient_table")
# @user_login_required
def patient_table():
    patient = Patient.query.all()

    return render_template("patient_table.html", patient=patient)


 
from sqlalchemy import func

@routes.route("/doctor_patient/<phone>")
def doctor_patient(phone):
    # Get doctor by phone (primary key)
    doctor = Doctor.query.get_or_404(phone)

    # Calculate average rating using phone as the reference
    avg_rating = db.session.query(func.avg(Rating.star))\
        .filter(Rating.doctor_id == doctor.phone).scalar()  # use doctor.phone

    avg_rating = round(avg_rating, 1) if avg_rating else 0

    return render_template("doctor_patient.html",
                           doctor=doctor,
                           avg_rating=avg_rating)


    
@routes.route('/final/<phone>')
@user_login_required
def final(phone):
    
    data = {
        "my_id": session.get('user_phone'),
        "target_id": phone,
        'role': session.get('role')
    }
    return render_template('final.html', data = data)


#delete account
@routes.route("/delete_account", methods=["POST"])
def delete_account():
    doctor_phone = session.get("doctor_phone")
    doctor = Doctor.query.get_or_404(doctor_phone)

    db.session.delete(doctor)
    db.session.commit()
    session.pop("doctor_phone", None)  # log out user
    flash("Your account has been deleted.")
    return redirect(url_for("routes.home"))
#edit account
@routes.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    doctor_phone = session.get("doctor_phone")  # or however you store logged-in user
    doctor = Doctor.query.get_or_404(doctor_phone)

    if request.method == "POST":
        doctor.name = request.form.get("full_name")
        doctor.specialization = request.form.get("specialization")
        # doctor.facebook = request.form.get("facebook")
        doctor.desc = request.form.get("desc")
        # Add other fields if needed
        db.session.commit()
        # flash("Profile updated successfully.")
        return redirect(url_for("routes.profileseenbydoctor", phone=doctor.phone))

    return render_template("edit_profile.html", doctor=doctor)
#change password
from werkzeug.security import generate_password_hash, check_password_hash

@routes.route("/change_password", methods=["GET", "POST"])
def change_password():
    doctor_phone = session.get("doctor_phone")
    doctor = Doctor.query.get_or_404(doctor_phone)

    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not check_password_hash(doctor.password, old_password):
            flash("Old password is incorrect")
            return redirect(url_for("routes.change_password"))

        if new_password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("routes.change_password"))

        doctor.password = generate_password_hash(new_password)
        db.session.commit()
        flash("Password changed successfully")
        return redirect(url_for("routes.profileseenbydoctor", phone=doctor.phone))

    return render_template("change_password.html")

@routes.route("/submit_rating", methods=["POST"])
def submit_rating():
    doctor_id = request.form.get("doctor_id")  
    star = request.form.get("star_rating")
    review = request.form.get("review_text")

    if not star or int(star) == 0:
        flash("Please select a star rating.")
        return redirect(request.referrer)

    new_rating = Rating(
        doctor_id=doctor_id,  
        star=int(star),
        review=review
    )

    db.session.add(new_rating)
    db.session.commit()

    flash("Rating submitted successfully!")
    return redirect(request.referrer)

from sqlalchemy import func

@routes.route("/submit_report", methods=["POST"])
@user_login_required
def submit_report():
    doctor_phone = request.form.get("doctor_id")
    reason = request.form.get("report_text")
    patient_phone = session.get("user_phone")  

    if not reason or reason.strip() == "":
        flash("Please provide a reason for the report.")
        return redirect(request.referrer)

    new_report = Report(
        doctor_id=doctor_phone,
        patient_id=patient_phone,
        reason=reason
    )

    db.session.add(new_report)
    db.session.commit()

    flash("Report submitted successfully!")
    return redirect(request.referrer)


@routes.route("/doctor/<int:id>")
def drprofile(id):  
    doctor = Doctor.query.get_or_404(id)
    avg_rating = db.session.query(func.avg(Rating.star))\
        .filter(Rating.doctor_phone == doctor.phone).scalar()
    avg_rating = round(avg_rating, 1) if avg_rating else 0

    return render_template("doctor_patient.html",
                           doctor=doctor,
                           avg_rating=avg_rating)








