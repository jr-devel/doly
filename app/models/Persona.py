from dataclasses import dataclass
from app.database import db

###
# DROP TABLE IF EXISTS Persona CASCADE;
# CREATE TABLE IF NOT EXISTS Persona (
#     id_persona SERIAL PRIMARY KEY,
#     full_name VARCHAR(100) NOT NULL,
#     birth_date DATE NOT NULL,
#     email VARCHAR(100) UNIQUE NOT NULL,
#     phone VARCHAR(15) NOT NULL,
#     CONSTRAINT chk_persona_full_name CHECK (LENGTH(full_name) BETWEEN 3 AND 100),
#     CONSTRAINT chk_persona_birth_date CHECK (birth_date <= CURRENT_DATE),
#     CONSTRAINT regex_persona_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
#     CONSTRAINT chk_persona_phone CHECK (phone IS NULL OR LENGTH(phone) BETWEEN 7 AND 15)
# );
###

@dataclass
class Persona(db.Model):
    __tablename__ = "persona"
    #-------------- Columns ------------------#
    id_persona = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('LENGTH(full_name) BETWEEN 3 AND 100', name='chk_persona_full_name'),
        db.CheckConstraint('birth_date <= CURRENT_DATE', name='chk_persona_birth_date'),
        db.CheckConstraint("LOWER(email) ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'", name='regex_persona_email'),
        db.CheckConstraint('LENGTH(phone) BETWEEN 7 AND 15', name='chk_persona_phone')
    )