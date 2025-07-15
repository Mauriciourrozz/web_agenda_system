from database.db import get_connection

def get_all_appointments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments ORDER BY fecha, hora")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def create_appointment(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO appointments (nombre_cliente, servicio, fecha, hora)
        VALUES (?, ?, ?, ?)
    ''', (data["nombre_cliente"], data["servicio"], data["fecha"], data["hora"]))
    conn.commit()
    conn.close()

def delete_appointment(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id = ?", (id,))
    conn.commit()
    conn.close()
