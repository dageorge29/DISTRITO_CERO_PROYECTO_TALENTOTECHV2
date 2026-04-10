from flask import Flask, render_template, request, jsonify
from contactDB import create_connection, create_table, insert_contact
import os

app = Flask(__name__)
app.secret_key = 'distrito_cero_key'

# 1. INICIALIZACIÓN DE LA BASE DE DATOS
# Esto asegura que la tabla exista en 'contact_form.db' al arrancar
def init_db():
    conn = create_connection()
    if conn:
        create_table(conn)
        conn.close()

init_db()

# 2. RUTAS DE NAVEGACIÓN
@app.route('/')
def index():
    # Flask busca automáticamente en la carpeta /templates
    return render_template('index.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/coleccion')
def coleccion():
    return render_template('coleccion.html')

# 3. RUTA DE CONTACTO (Maneja GET para ver la página y POST para guardar datos)
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        # Intentamos obtener datos ya sea por JSON (Fetch API) o por Formulario tradicional
        if request.is_json:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')
        else:
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')

        # Validación básica
        if name and email and message:
            try:
                conn = create_connection()
                if conn:
                    insert_contact(conn, name, email, message)
                    conn.close()
                    return jsonify({
                        "status": "success", 
                        "message": "¡Mensaje guardado! Gracias por contactar a Distrito Cero."
                    }), 200
            except Exception as e:
                return jsonify({"status": "error", "message": f"Error de DB: {str(e)}"}), 500
        
        return jsonify({"status": "error", "message": "Por favor, completa todos los campos."}), 400

    # Si es GET, simplemente muestra la página
    return render_template('contacto.html')

# 4. LANZAMIENTO DEL SERVIDOR
if __name__ == '__main__':
    # Puerto 5501 para que coincida con tu entorno de desarrollo
    # '0.0.0.0' permite que otros dispositivos en tu red vean la app si lo necesitas
    app.run(host='0.0.0.0', port=5501, debug=True)