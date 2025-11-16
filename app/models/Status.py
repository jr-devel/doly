from dataclasses import dataclass
from app.database import db

###
# DROP TABLE IF EXISTS Status CASCADE;
# CREATE TABLE IF NOT EXISTS Status (
#     id_status SERIAL PRIMARY KEY,
#     name VARCHAR(50) NOT NULL,
#     CONSTRAINT chk_status_name CHECK (LENGTH(name) >= 3 AND LENGTH(name) <= 50),
#     CONSTRAINT regex_status_name_no_whitespace CHECK (name !~* '\s{2,}'),
#     CONSTRAINT regex_status_name_format CHECK (name ~* '^[A-Za-z]+$')
# );
###

@dataclass
class Status(db.Model):
    __tablename__ = "status"
    #-------------- Columns ------------------#
    id_status = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('LENGTH(name) >= 3 AND LENGTH(name) <= 50', name='chk_status_name'),
        db.CheckConstraint("name !~* '\\s{2,}'", name='regex_status_name_no_whitespace'),
        db.CheckConstraint("name ~* '^[A-Za-z ]+$'", name='regex_status_name_format'),
    )