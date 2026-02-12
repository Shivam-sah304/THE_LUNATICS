
from flask import Flask, redirect, request, jsonify, session, url_for

import config
from models import Doctor
from werkzeug.security import check_password_hash

from functools import wraps
from routes import routes
# app = Flask(__name__)

from datetime import timedelta
config.SECRET_KEY 

# Doctor Login route - issues JWT token
