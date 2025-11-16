from dataclasses import dataclass
from app.database import db

###
# DROP TABLE IF EXISTS EmployeeType CASCADE;
# CREATE TABLE IF NOT EXISTS EmployeeType (
#     id_employee_type SERIAL PRIMARY KEY,
#     name VARCHAR(50) NOT NULL,
#     CONSTRAINT chk_employee_type_name CHECK(LENGTH(name) >= 3 AND LENGTH(name) <= 50)
# );
###

@dataclass
class EmployeeType(db.Model):
    __tablename__ = "employeetype"
    #-------------- Columns ------------------#
    id_employee_type = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('LENGTH(name) >= 3 AND LENGTH(name) <= 50', name='chk_employee_type_name'),
    )