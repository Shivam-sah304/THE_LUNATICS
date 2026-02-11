from flask import Blueprint, render_template, request, redirect, session,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os



from models import db, Doctor

routes = Blueprint("routes", __name__)
@routes.route("/")
def home():
    return render_template("index.html")

@routes.route("/doctorregistration", methods=["GET", "POST"])
def doctorregistration():
    if request.method == "POST":
        # Get data from form
        name = request.form["fullname"]          # form uses 'fullname' but model uses 'name'
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]
        dob = datetime.strptime(request.form["dob"], "%Y-%m-%d").date()
        desc = request.form.get("about")         # optional
        degree = request.form["education"]
        experience = request.form["experience"]
        specialization = request.form.get("specialization")  # optional

        # Create Doctor object using model column names
        doctor = Doctor(
            name=name,
            email=email,
            phone=phone,
            address=address,
            dob=dob,
            desc=desc,
            degree=degree,
            experience=experience,
            specialization=specialization
        )

        db.session.add(doctor)
        db.session.commit()
        return redirect(url_for('routes.home'))

    return render_template("doctorregistration.html")