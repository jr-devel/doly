from dataclasses import dataclass
from app.database import db

###
# DROP TABLE IF EXISTS Evidence CASCADE; -- Evidence can be from Client or Employee -- FIXED
# CREATE TABLE IF NOT EXISTS Evidence (
#     id_evidence SERIAL PRIMARY KEY,
#     user_id INT NOT NULL,
#     file_path VARCHAR(255) NOT NULL,
#     file_name VARCHAR(38) NOT NULL,
#     process VARCHAR(50) NOT NULL, -- upload, service_start, service_end, etc.
#     upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     CONSTRAINT fk_evidence_user_id FOREIGN KEY (user_id) REFERENCES UserAccount(id_user) ON DELETE RESTRICT,
#     CONSTRAINT chk_evidence_file_path_length CHECK (LENGTH(file_path) <= 255),
#     CONSTRAINT chk_evidence_file_name_length CHECK (LENGTH(file_name) <= 38),
#     CONSTRAINT chk_evidence_process_length CHECK (LENGTH(process) <= 50),
#     CONSTRAINT regex_evidence_file_path_no_whitespace CHECK (file_path !~* '\s'),
#     CONSTRAINT regex_evidence_file_name_no_whitespace CHECK (file_name !~* '\s')
# );
###

#EVIDENCE FILENAME INSTANCE
# EX: EV AA BB YYYYMMDD HHMMSS CCCCCCCCC DD EEEEEE.ext
# -- EV: Evidence Prefix
# AA: Arribo -> 'AR', Termino -> 'TR'
# BB: Numero de instancia de arribo o termino -> '01', '02', etc.
# YYYYMMDD: Fecha de arribo o termino
# HHMMSS: Hora de arribo o termino
# CCCCCCCCC: ID de usuario (Client o Employee) con ceros a la izquierda hasta completar 9 digitos
# DD: Tipo de Usuario (Client -> 'CL', Employee -> 'EM')
# EEEEEE: ultimos 6 dígitos de vin del vehículo
# .ext: Extension del archivo

@dataclass
class Evidence(db.Model):
    __tablename__ = "evidence"
    #-------------- Columns ------------------#
    id_evidence = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('useraccount.id_user', ondelete='RESTRICT'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(38), nullable=False)
    process = db.Column(db.String(50), nullable=False)
    upload_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('LENGTH(file_path) <= 255', name='chk_evidence_file_path_length'),
        db.CheckConstraint('LENGTH(file_name) <= 38', name='chk_evidence_file_name_length'),
        db.CheckConstraint('LENGTH(process) <= 50', name='chk_evidence_process_length'),
        db.CheckConstraint("file_path !~* '\\s'", name='regex_evidence_file_path_no_whitespace'),
        db.CheckConstraint("file_name !~* '\\s'", name='regex_evidence_file_name_no_whitespace'),
        db.UniqueConstraint('file_path', 'file_name', name='unique_evidence_filepath_filename'),
    )