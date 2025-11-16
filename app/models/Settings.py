from dataclasses import dataclass
from app.database import db

# Settings table per DDL

@dataclass
class Settings(db.Model):
    __tablename__ = 'settings'
    #-------------- Columns ------------------#
    id_setting = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id_company', ondelete='CASCADE'), nullable=False)
    setting_key = db.Column(db.String(50), nullable=False)
    setting_value = db.Column(db.String(255))
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.UniqueConstraint('company_id', 'setting_key', name='uq_company_setting_key'),
        db.CheckConstraint('LENGTH(setting_key) BETWEEN 3 AND 50', name='chk_settings_key_length'),
        db.CheckConstraint('setting_value IS NULL OR LENGTH(setting_value) <= 255', name='chk_settings_value_length'),
        db.CheckConstraint('company_id > 0', name='chk_settings_company_id_positive'),
        db.CheckConstraint("setting_key ~ '^[a-z0-9_]+$'", name='chk_settings_key_format'),
        db.CheckConstraint('setting_key = lower(setting_key)', name='chk_settings_key_lowercase'),
        db.CheckConstraint('setting_value IS NULL OR trim(setting_value) = setting_value', name='chk_settings_value_trimmed'),
    )
