from flask import Blueprint, request, jsonify
from models.appointment import get_all_appointments, create_appointment, delete_appointment
from utils.validators import (
    is_slot_available,
    is_valid_service,
    is_valid_slot_time,
    is_valid_time_format,
    is_valid_day,
    get_available_slots
)

appointments = Blueprint("appointments", __name__)

@appointments.route("/turnos", methods=["GET"])
def listar_turnos():
    return jsonify(get_all_appointments())

@appointments.route("/turnos", methods=["POST"])
def crear_turno():
    data = request.get_json()

    if not is_valid_service(data.get("servicio", "")):
        return jsonify({"error": "Servicio inválido"}), 400

    if not is_valid_time_format(data.get("hora", "")) or not is_valid_slot_time(data["hora"]):
        return jsonify({
            "error": "Hora inválida. Debe estar entre 08:00 y 20:00, en intervalos de 30 minutos"
        }), 400

    if not is_valid_day(data.get("fecha", "")):
        return jsonify({"error": "Los turnos solo pueden agendarse de lunes a sábado"}), 400

    if not is_slot_available(data["fecha"], data["hora"]):
        return jsonify({"error": "Turno no disponible"}), 400

    create_appointment(data)
    return jsonify({"message": "Turno creado exitosamente"}), 201

@appointments.route("/turnos/<int:id>", methods=["DELETE"])
def cancelar_turno(id):
    delete_appointment(id)
    return jsonify({"message": "Turno cancelado"}), 200

@appointments.route("/turnos/disponibles", methods=["GET"])
def horarios_disponibles():
    fecha = request.args.get("fecha")
    if not fecha or not is_valid_day(fecha):
        return jsonify({"error": "Fecha inválida o es domingo"}), 400

    horarios = get_available_slots(fecha)
    return jsonify({
        "fecha": fecha,
        "disponibles": horarios
    }), 200
