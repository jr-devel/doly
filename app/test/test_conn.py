import os
import psycopg2 as db

def load_dotenv_file():
    load_dotenv = False
    try:
        from dotenv import load_dotenv as ld
        ld()
        load_dotenv = True
    except Exception as e:
        print(f"No se pudo cargar el archivo .env\nException: {e}")
    return load_dotenv

def test_conn():
    if load_dotenv_file():
        dsn = os.getenv('DATABASE_URL')
        try:
            with db.connect(dsn) as conn:
                with conn.cursor() as c:
                    c.execute('SELECT VERSION();')
                    version = c.fetchone()
                    print(f"PostgreSQL version: {version[0]}")
                    return True
            print("✅ Conectado correctamente a la base de datos Neon.tech")
        except Exception as e:
            print("❌ Error al conectar con Neon.tech:", e)
            return False

if __name__ == '__main__':
    print(f"Conexion exitosa: {test_conn()}")