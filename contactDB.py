import sqlite3

DATABASE_NAME = 'contact_form.db'

def create_connection():
    """Crea una conexión a la base de datos SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return conn

def create_table(conn):
    """Crea la tabla 'contacts' si no existe."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        print("Tabla 'contacts' creada o ya existente.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla: {e}")

def insert_contact(conn, name, email, message):
    """Inserta un nuevo registro de contacto en la tabla 'contacts'."""
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name, email, message))
        conn.commit()
        print(f"Contacto de {name} insertado exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al insertar contacto: {e}")

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        create_table(conn)

        # Ejemplo de cómo insertar datos
        print("\nInsertando contactos de ejemplo:")
        insert_contact(conn, "Juan Pérez", "juan.perez@example.com", "Me gustaría saber más sobre sus servicios.")
        insert_contact(conn, "María García", "maria.garcia@example.com", "Tengo una pregunta sobre la colección.")

        # Opcional: Verificar los datos insertados
        print("\nDatos actuales en la tabla 'contacts':")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        conn.close()
        print("\nConexión a la base de datos cerrada.")