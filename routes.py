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

@routes.route("/doctorregistration",methods=["GET","POST"])
def doctorregistration():
    if request.method=="POST":
        name=request.form["full_name"]
        email=request.form["email"]
        phone=request.form["phone"]
        address=request.form["address"]
        dob=datetime.strptime(request.form["dob"], "%Y-%m-%d").date()
        desc=request.form["about"]
        degree=request.form["education"]
        experience=request.form["experience"]
        

