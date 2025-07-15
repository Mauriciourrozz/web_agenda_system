from database.db import get_connection
from datetime import datetime, time, timedelta

# Lista de servicios válidos
VALID_SERVICES = [
    "corte",
    "corte + barba",
    "corte + mechas",
    "corte + full color"
]

# Verifica si ya hay turno en esa fecha y hora
def is_slot_available(fecha, hora):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments WHERE fecha = ? AND hora = ?", (fecha, hora))
    exists = cursor.fetchone()
    conn.close()
    return exists is None

# Verifica que el servicio sea válido
def is_valid_service(servicio):
    return servicio.lower().strip() in VALID_SERVICES

# Verifica que la hora tenga formato correcto
def is_valid_time_format(hora):
    try:
        datetime.strptime(hora, "%H:%M")
        return True
    except ValueError:
        return False

# Verifica que la hora esté entre 08:00 y 20:00, en intervalos de 30 minutos
def is_valid_slot_time(hora):
    try:
        hora_obj = datetime.strptime(hora, "%H:%M").time()
        hora_inicio = time(8, 0)
        hora_fin = time(20, 0)
        minutos_validos = hora_obj.minute in [0, 30]
        return hora_inicio <= hora_obj <= hora_fin and minutos_validos
    except:
        return False

# 🔴 Verifica que la fecha no sea domingo
def is_valid_day(fecha):
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        return fecha_obj.weekday() < 6  # 0=Lunes ... 6=Domingo → solo true si es de Lunes a Sábado
    except ValueError:
        return False

def get_available_slots(dates):
    horarios = []
    hora = time(8, 0)
    fin = time(20, 0)

    while hora < fin:
        if is_slot_available(dates, hora.strftime("%H:%M")):
            horarios.append(hora.strftime("%H:%M"))
        # sumar 30 minutos
        hora_dt = datetime.combine(datetime.today(), hora) + timedelta(minutes=30)
        hora = hora_dt.time()
    
    return horarios
