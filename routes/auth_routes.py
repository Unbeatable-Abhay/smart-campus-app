from flask import Blueprint, request, jsonify
from models.user import create_user, get_user_by_email, check_password
from utils.auth_utils import generate_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")
    department = data.get("department")

    if not name or not email or not password or not role:
        return jsonify({"error": "name, email, password, and role are required"}), 400

    if role not in ["student", "faculty", "admin"]:
        return jsonify({"error": "role must be student, faculty, or admin"}), 400

    existing_user = get_user_by_email(email)
    if existing_user is not None:
        return jsonify({"error": "A user with this email already exists"}), 409

    new_user_id = create_user(name, email, password, role, department)

    return jsonify({"message": "User registered successfully", "user_id": new_user_id}), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = get_user_by_email(email)
    if user is None:
        return jsonify({"error": "Invalid email or password"}), 401

    password_matches = check_password(password, user["password_hash"])
    if not password_matches:
        return jsonify({"error": "Invalid email or password"}), 401

    token = generate_token(user["id"], user["role"])

    return jsonify({
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "department": user["department"]
        }
    }), 200