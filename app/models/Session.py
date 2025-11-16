from dataclasses import dataclass
from app.database import db

###
# DROP TABLE IF EXISTS Session CASCADE;
# CREATE TABLE IF NOT EXISTS Session (
#     id_session SERIAL PRIMARY KEY,
#     user_id INT NOT NULL,
#     token VARCHAR(255) UNIQUE NOT NULL,
#     login_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     logout_time TIMESTAMP,
#     active BOOLEAN NOT NULL DEFAULT TRUE,
#     ip_address VARCHAR(45),         -- opcional: IPv4/IPv6
#     user_agent VARCHAR(255),        -- opcional: navegador/dispositivo
#     last_used_at TIMESTAMP,         -- opcional: último uso / actividad
#     CONSTRAINT fk_session_user_id FOREIGN KEY (user_id) REFERENCES UserAccount(id_user) ON DELETE CASCADE,
#     CONSTRAINT chk_session_token_length CHECK (char_length(token) BETWEEN 8 AND 255),
#     CONSTRAINT regex_session_token_no_whitespace CHECK (trim(token) = token AND token !~* '\s'),
#     CONSTRAINT chk_session_token_charset CHECK (token ~* '^[A-Za-z0-9._\-=]+$'),
#     CONSTRAINT chk_session_user_id_positive CHECK (user_id > 0),
#     CONSTRAINT chk_session_created_at_past CHECK (login_time <= CURRENT_TIMESTAMP),
#     CONSTRAINT chk_session_expires_after_created CHECK (logout_time IS NULL OR logout_time > login_time),
#     CONSTRAINT chk_session_active_expiration CHECK (active = FALSE OR logout_time IS NULL OR logout_time > CURRENT_TIMESTAMP),
#     CONSTRAINT chk_ip_address_format CHECK (ip_address IS NULL OR ip_address ~ '^[0-9A-Fa-f:\\.]+$'),
#     CONSTRAINT chk_user_agent_length CHECK (user_agent IS NULL OR char_length(user_agent) <= 255)
# );
###

@dataclass
class Session(db.Model):
    __tablename__ = "session"
    #-------------- Columns ------------------#
    id_session = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('useraccount.id_user', ondelete='CASCADE'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    login_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    logout_time = db.Column(db.DateTime)
    active = db.Column(db.Boolean, nullable=False, default=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    last_used_at = db.Column(db.DateTime)
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('char_length(token) BETWEEN 8 AND 255', name='chk_session_token_length'),
        db.CheckConstraint("trim(token) = token AND token !~* '\\s'", name='regex_session_token_no_whitespace'),
        db.CheckConstraint("token ~* '^[A-Za-z0-9._\\-=]+$'", name='chk_session_token_charset'),
        db.CheckConstraint('user_id > 0', name='chk_session_user_id_positive'),
        db.CheckConstraint('login_time <= CURRENT_TIMESTAMP', name='chk_session_created_at_past'),
        db.CheckConstraint('logout_time IS NULL OR logout_time > login_time', name='chk_session_expires_after_created'),
        db.CheckConstraint('active = FALSE OR logout_time IS NULL OR logout_time > CURRENT_TIMESTAMP', name='chk_session_active_expiration'),
        db.CheckConstraint("ip_address IS NULL OR ip_address ~ '^[0-9A-Fa-f:\\\\.]+$'", name='chk_ip_address_format'),
        db.CheckConstraint('user_agent IS NULL OR char_length(user_agent) <= 255', name='chk_user_agent_length')
    )