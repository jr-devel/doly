from dataclasses import dataclass
from app.database import db

@dataclass
class Client(db.Model):
    __tablename__ = 'client'
    #-------------- Columns ------------------#
    id_client = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('useraccount.id_user', ondelete='CASCADE'), nullable=False)
    ine = db.Column(db.Boolean, server_default=db.text('FALSE'))
    client_type = db.Column(db.Integer, db.ForeignKey('clienttype.id_client_type', ondelete='SET NULL'))
    license_number = db.Column(db.String(20))
    message_permission = db.Column(db.Boolean, server_default=db.text('FALSE'))
    terms_agreement = db.Column(db.Boolean, server_default=db.text('FALSE'))
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('LENGTH(license_number) <= 20', name='chk_client_license_number'),
        db.CheckConstraint("license_number IS NULL OR license_number ~* '^[A-Za-z0-9-]+$'", name='chk_client_license_number_format'),
        db.CheckConstraint("license_number IS NULL OR license_number !~* '\\s'", name='regex_client_license_number_no_whitespace'),
        db.CheckConstraint('user_id > 0', name='chk_client_user_id_positive'),
    )