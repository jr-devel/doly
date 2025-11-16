from dataclasses import dataclass
from app.database import db

###
# DROP TABLE IF EXISTS Company CASCADE;
# CREATE TABLE IF NOT EXISTS Company (
#     id_company SERIAL PRIMARY KEY,
#     legal_name VARCHAR(100) NOT NULL,
#     common_name VARCHAR(100),
#     total_services INT DEFAULT 0,
#     total_assistances INT DEFAULT 0,
#     fiscal_address VARCHAR(255),
#     base_address VARCHAR(255),
#     CONSTRAINT chk_company_legal_name CHECK (LENGTH(legal_name) BETWEEN 3 AND 100),
#     CONSTRAINT chk_company_common_name CHECK (common_name IS NULL OR LENGTH(common_name) <= 100)
# );
###

@dataclass
class Company(db.Model):
    __tablename__ = 'company'
    #-------------- Columns ------------------#
    id_company = db.Column(db.Integer, primary_key=True, autoincrement=True)
    legal_name = db.Column(db.String(100), nullable=False)
    common_name = db.Column(db.String(100))
    total_services = db.Column(db.Integer, server_default=db.text('0'))
    total_assistances = db.Column(db.Integer, server_default=db.text('0'))
    fiscal_address = db.Column(db.String(255))
    base_address = db.Column(db.String(255))
    rating_avg = db.Column(db.Numeric(3, 2), server_default=db.text('0'))
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('rating_avg BETWEEN 0 AND 5', name='chk_company_rating_avg'),
        db.CheckConstraint('total_services >= 0', name='chk_company_total_services'),
        db.CheckConstraint('total_assistances >= 0', name='chk_company_total_assistances'),
        db.CheckConstraint('fiscal_address IS NULL OR LENGTH(fiscal_address) <= 255', name='chk_company_fiscal_address'),
        db.CheckConstraint('base_address IS NULL OR LENGTH(base_address) <= 255', name='chk_company_base_address'),
        db.CheckConstraint('LENGTH(legal_name) BETWEEN 3 AND 100', name='chk_company_legal_name'),
        db.CheckConstraint('common_name IS NULL OR LENGTH(common_name) <= 100', name='chk_company_common_name'),
    )