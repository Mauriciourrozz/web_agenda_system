from flask import Flask
from flask_cors import CORS
from database.db import init_db
from routes.appointments import appointments
from routes.admin import admin_bp

app = Flask(__name__)
CORS(app, supports_credentials=True) 

app.secret_key = "17deenero"

init_db()

# Registra las rutas
app.register_blueprint(appointments)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)
