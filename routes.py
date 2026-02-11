from flask import Blueprint, render_template, request, redirect, session,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
# from rembg import remove
# from PIL import Image
# import uuid


from models import db, Doctor,Patient

routes = Blueprint("routes", __name__)
