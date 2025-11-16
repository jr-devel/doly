from dataclasses import dataclass
from app.database import db

# Service_Discount table per DDL

@dataclass
class Service_Discount(db.Model):
    __tablename__ = 'service_discount'
    #-------------- Columns ------------------#
    id_service_discount = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id_service', ondelete='CASCADE'), nullable=False)
    discount_id = db.Column(db.Integer, db.ForeignKey('discount.id_discount', ondelete='CASCADE'), nullable=False)
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.UniqueConstraint('service_id', 'discount_id', name='uq_service_discount'),
        db.CheckConstraint('service_id > 0 AND discount_id > 0', name='chk_service_discount_positive'),
    )
