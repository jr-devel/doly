from dataclasses import dataclass
from app.database import db

###
# DROP TABLE IF EXISTS UserAccount CASCADE;
# CREATE TABLE IF NOT EXISTS UserAccount (
#     id_user SERIAL PRIMARY KEY,
#     username VARCHAR(30) UNIQUE NOT NULL,
#     password VARCHAR(100) NOT NULL,
#     role VARCHAR(30) NOT NULL,  -- client, employee, admin, etc.
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     persona_id INT NOT NULL,
#     CONSTRAINT fk_user_persona_id FOREIGN KEY (persona_id) REFERENCES Persona(id_persona) ON DELETE CASCADE,
#     CONSTRAINT chk_user_username CHECK (LENGTH(username) BETWEEN 4 AND 30),
#     CONSTRAINT chk_user_password CHECK (LENGTH(password) BETWEEN 8 AND 100),
#     CONSTRAINT chk_user_role CHECK (
#         role IN (
#             'client',
#             'employee',
#             'company_admin',
#             'sys_admin',
#             'audit_admin',
#             'support_staff'
#         )
#     ),
#     CONSTRAINT regex_user_username_no_space CHECK (username !~* '\s')
# );
###

@dataclass
class UserAccount(db.Model):
    __tablename__ = "useraccount"
    #-------------- Columns ------------------#
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False)  # client, employee, admin, etc.
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id_persona', ondelete='CASCADE'), nullable=False)
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('LENGTH(username) BETWEEN 4 AND 30', name='chk_user_username'),
        db.CheckConstraint(
            "role IN ('client', 'employee', 'company_admin', 'sys_admin', 'audit_admin', 'support_staff')",
            name='chk_user_role'
        ),
        db.CheckConstraint("username !~* '\\s'", name='regex_user_username_no_space'),
    )