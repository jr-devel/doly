from dataclasses import dataclass
from app.database import db

# Resource_Company table per DDL

@dataclass
class Resource_Company(db.Model):
    __tablename__ = 'resource_company'
    #-------------- Columns ------------------#
    id_resource_company = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id_resource', ondelete='CASCADE'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id_company', ondelete='CASCADE'), nullable=False)
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.UniqueConstraint('resource_id', 'company_id', name='uq_resource_company'),
        db.CheckConstraint('resource_id > 0 AND company_id > 0', name='chk_resource_company'),
    )
