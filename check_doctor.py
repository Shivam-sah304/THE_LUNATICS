import os
from flask import Flask, jsonify, redirect, url_for

from flask import Blueprint, request



routes = Blueprint("routes", __name__)


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
routes.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@routes.route('/drvalidation', methods=['POST'])
def check_doctor():
  doctor_photo = request.files.get("doctor_photo")
  nmc_license = request.files.get("nmc_license")
  nmc_number = request.form.get("nmc_number")
  
  if not doctor_photo or not nmc_license or not nmc_number:
      return jsonify({"message": "All fields are required"}), 400
  
  try:
    doctor_photo.save(os.path.join(routes.config["UPLOAD_FOLDER"], doctor_photo.filename))
    nmc_license.save(os.path.join(routes.config["UPLOAD_FOLDER"], nmc_license.filename))

    print("NMC Number:", nmc_number)
    

    return jsonify({"message": "Validation successful"}), 200

  except Exception:
    return jsonify({"message": "Error saving files"}), 500