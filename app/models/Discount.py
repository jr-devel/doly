from dataclasses import dataclass
from app.database import db

# Discount table per DDL

@dataclass
class Discount(db.Model):
    __tablename__ = 'discount'
    #-------------- Columns ------------------#
    id_discount = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(500))
    percentage = db.Column(db.Numeric(5, 2), nullable=False, server_default=db.text('0'))
    valid_from = db.Column(db.Date)
    valid_to = db.Column(db.Date)
    active = db.Column(db.Boolean, nullable=False, server_default=db.text('TRUE'))
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('char_length(code) BETWEEN 3 AND 50', name='chk_discount_code_length'),
        db.CheckConstraint("code ~ '^[a-z0-9_]+$'", name='chk_discount_code_format'),
        db.CheckConstraint('code = lower(trim(code))', name='chk_discount_code_normalized'),
        db.CheckConstraint('description IS NULL OR trim(description) = description', name='chk_discount_description_trimmed'),
        db.CheckConstraint('percentage >= 0 AND percentage <= 100', name='chk_discount_percentage_range'),
        db.CheckConstraint('valid_from IS NULL OR valid_to IS NULL OR valid_from <= valid_to', name='chk_discount_dates_valid'),
    )
