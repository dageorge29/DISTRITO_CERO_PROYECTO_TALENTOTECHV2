from flask import Flask, render_template, request, jsonify
from contactDB import create_connection, create_table, insert_contact
import os

app = Flask(__name__)
app.secret_key = 'distrito_cero_key'

# Inicializar la base de datos al arrancar la aplicación
def init_db():
    conn = create_connection()
    if conn:
        create_table(conn)
        conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/coleccion')
def coleccion():
    return render_template('coleccion.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        # Obtener datos del formulario (form-data o JSON)
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if name and email and message:
            conn = create_connection()
            if conn:
                insert_contact(conn, name, email, message)
                conn.close()
                return jsonify({"status": "success", "message": "Datos guardados correctamente"}), 200
        
        return jsonify({"status": "error", "message": "Faltan campos obligatorios"}), 400

    return render_template('contacto.html')

if __name__ == '__main__':
    app.run(debug=True)