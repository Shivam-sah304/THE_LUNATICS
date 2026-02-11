from flask import Flask, redirect, request, jsonify, session, url_for

import config
from models import Doctor
from werkzeug.security import check_password_hash

from functools import wraps

app = Flask(__name__)

from datetime import timedelta
config.SECRET_KEY 

# Doctor Login route - issues JWT token
@app.route('/drlogin', methods=['POST'])
def login():
    phone = request.json.get('phone')
    password = request.json.get('password')

    user = Doctor.query.filter_by(phone=phone).first()

    if user and check_password_hash(user.password, password):
        session["user_id"] = user.phone
        return redirect(url_for('routes.home'))
    else:
        return "Invalid phone or password"  



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("routes.doctorlogin"))  # redirect to login if not logged in
        return f(*args, **kwargs)
    return decorated_function
