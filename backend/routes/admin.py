from flask import Blueprint, request, jsonify, session
from auth.admin import verify_credentials
from models.appointment import get_all_appointments

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/login", methods=["POST"])
def login_admin():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if verify_credentials(username, password):
        session["admin"] = True
        return jsonify({"message": "Login exitoso"}), 200

    return jsonify({"error": "Credenciales inválidas"}), 401

@admin_bp.route("/admin/logout", methods=["POST"])
def logout_admin():
    session.pop("admin", None)
    return jsonify({"message": "Sesión cerrada"}), 200

@admin_bp.route("/admin/turnos", methods=["GET"])
def turnos_admin():
    if not session.get("admin"):
        return jsonify({"error": "No autorizado"}), 403

    return jsonify(get_all_appointments()), 200
