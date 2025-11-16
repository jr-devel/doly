import os

load_dotenv = False
try:
    from dotenv import load_dotenv as ld
    ld()
    load_dotenv = True
except ImportError:
    print("No se pudo cargar el archivo .env")

if __name__ == '__main__':
    if load_dotenv:
        print(f"FLASK ENV: {os.getenv('FLASK_ENV')}")
        print(f"SECRET KEY: {os.getenv('SECRET_KEY')}")
        print(f"DATABASE URL: {os.getenv('DATABASE_URL')}")