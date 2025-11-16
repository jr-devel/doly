from dataclasses import dataclass
from app.database import db

@dataclass
class Tracking(db.Model):
	__tablename__ = 'tracking'
	#-------------- Columns ------------------#
	id_tracking = db.Column(db.Integer, primary_key=True, autoincrement=True)
	service_id = db.Column(db.Integer, db.ForeignKey('service.id_service', ondelete='CASCADE'), nullable=False)
	latitude = db.Column(db.Numeric(10, 8))
	longitude = db.Column(db.Numeric(11, 8))
	updated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
	#-------------- Constraints ------------------#
	__table_args__ = (
		db.CheckConstraint('service_id > 0', name='chk_tracking_service_id_positive'),
		db.CheckConstraint('latitude IS NULL OR latitude BETWEEN -90 AND 90', name='chk_tracking_latitude_range'),
		db.CheckConstraint('longitude IS NULL OR longitude BETWEEN -180 AND 180', name='chk_tracking_longitude_range'),
		db.CheckConstraint('updated_at <= CURRENT_TIMESTAMP', name='chk_tracking_updated_at_past'),
	)