from dataclasses import dataclass
from app.database import db

# ServiceType table per DDL

@dataclass
class ServiceType(db.Model):
    __tablename__ = 'servicetype'
    #-------------- Columns ------------------#
    id_service_type = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('LENGTH(name) BETWEEN 3 AND 100', name='chk_service_type_name'),
        db.CheckConstraint('LENGTH(description) BETWEEN 10 AND 500', name='chk_service_type_description'),
    )
