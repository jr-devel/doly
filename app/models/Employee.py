from dataclasses import dataclass
from app.database import db

###
# DROP TABLE IF EXISTS Employee CASCADE;
# CREATE TABLE IF NOT EXISTS Employee (
#     id_employee SERIAL PRIMARY KEY,
#     user_id INT NOT NULL,
#     employee_type_id INT NOT NULL,
#     CONSTRAINT fk_employee_user_id FOREIGN KEY (user_id) REFERENCES UserAccount(id_user) ON DELETE CASCADE,
#     CONSTRAINT fk_employee_type_id FOREIGN KEY (employee_type_id) REFERENCES EmployeeType(id_employee_type),
#     CONSTRAINT chk_employee_type_id CHECK (employee_type_id > 0)
# );
###

@dataclass
class Employee(db.Model):
    __tablename__ = "employee"
    #-------------- Columns ------------------#
    id_employee = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('useraccount.id_user', ondelete='CASCADE'), nullable=False)
    employee_type_id = db.Column(db.Integer, db.ForeignKey('employeetype.id_employee_type', ondelete='CASCADE'), nullable=False)
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('employee_type_id > 0', name='chk_employee_type_id'),
    )