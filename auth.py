from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your-secret-key"  # Change this
jwt = JWTManager(app)


# Doctor Login route - issues JWT token
@app.route('/drlogin', methods=['POST'])
def login():
    user_id = request.json.get('phone')
    password = request.json.get('password')

    user = Doctor.query.filter_by(phone=phone).first()
    # Dummy check – replace with DB check
    if user_id == "samir" and password == "password123":
        access_token = create_access_token(identity=user_id)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad username or password"}), 401

