from dataclasses import dataclass
from app.database import db

# Assistance table per DDL

@dataclass
class Assistance(db.Model):
    __tablename__ = 'assistance'
    #-------------- Columns ------------------#
    id_assistance = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id_service', ondelete='CASCADE'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.text('0'))
    tax = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.text('0'))
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('cost >= 0', name='chk_assistance_cost_non_negative'),
        db.CheckConstraint('tax >= 0', name='chk_assistance_tax_non_negative'),
        db.CheckConstraint('service_id > 0', name='chk_assistance_service_id_positive'),
        db.CheckConstraint('LENGTH(description) <= 500', name='chk_assistance_description_length'),
        db.CheckConstraint("description !~* '\\s{2,}'", name='chk_assistance_description_whitespace'),
        db.CheckConstraint("description ~* '^[A-Za-z0-9 .,;:!?()-]*$'", name='chk_assistance_description_charset'),
    )
