from sqlalchemy import *
from sqlalchemy.orm import *
from app.database import db
from app.Models.Company import Company
from app.Models.Employee import Employee
from dataclasses import dataclass

###
# DROP TABLE IF EXISTS Company_Employee CASCADE;
# CREATE TABLE IF NOT EXISTS Company_Employee (
#     id_company_employee SERIAL PRIMARY KEY,
#     company_id INT NOT NULL,
#     employee_id INT NOT NULL,
#     CONSTRAINT fk_company_employee_company_id FOREIGN KEY (company_id) REFERENCES Company(id_company) ON DELETE CASCADE,
#     CONSTRAINT fk_company_employee_employee_id FOREIGN KEY (employee_id) REFERENCES Employee(id_employee) ON DELETE CASCADE,
#     UNIQUE (company_id, employee_id),
#     CONSTRAINT chk_company_employee CHECK (company_id > 0 AND employee_id > 0)
# );
###

@dataclass
class Company_Employee(db.Model):
    __tablename__ = 'company_employee'
    #-------------- Columns ------------------#
    id_company_employee = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, db.ForeignKey('company.id_company', ondelete='CASCADE'), nullable=False)
    employee_id = Column(Integer, db.ForeignKey('employee.id_employee', ondelete='CASCADE'), nullable=False)
    #-------------- Constraints ------------------#
    __table_args__ = (
        UniqueConstraint('company_id', 'employee_id', name='uq_company_employee'),
        CheckConstraint('company_id > 0 AND employee_id > 0', name='chk_company_employee')
    )