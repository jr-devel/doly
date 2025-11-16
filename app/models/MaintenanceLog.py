from dataclasses import dataclass
from app.database import db

# MaintenanceLog table per DDL

@dataclass
class MaintenanceLog(db.Model):
    __tablename__ = 'maintenancelog'
    #-------------- Columns ------------------#
    id_maintenance = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id_resource', ondelete='CASCADE'), nullable=False)
    maintenance_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    performed_by = db.Column(db.String(100))
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('resource_id > 0', name='chk_maintenance_resource_id_positive'),
        db.CheckConstraint('maintenance_date <= CURRENT_DATE', name='chk_maintenance_date_past'),
        db.CheckConstraint('performed_by IS NULL OR LENGTH(performed_by) <= 100', name='chk_maintenance_performed_by_length'),
        db.CheckConstraint('description IS NULL OR LENGTH(description) <= 500', name='chk_maintenance_description_length'),
        db.CheckConstraint('description IS NULL OR trim(description) = description', name='chk_maintenance_description_trimmed'),
        db.CheckConstraint("description IS NULL OR description !~* '\\s{2,}'", name='chk_maintenance_description_no_multispaces'),
        db.CheckConstraint("description IS NULL OR description ~* '^[A-Za-z0-9 .,;:!?()\\n-]*$'", name='chk_maintenance_description_charset'),
        db.CheckConstraint('performed_by IS NULL OR trim(performed_by) = performed_by', name='chk_maintenance_performed_by_trimmed'),
        db.CheckConstraint("performed_by IS NULL OR performed_by !~* '\\s{2,}'", name='chk_maintenance_performed_by_no_multispaces'),
    )
