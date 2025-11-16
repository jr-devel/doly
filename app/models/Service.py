from dataclasses import dataclass
from app.database import db

###
# Service table per DDL
###

@dataclass
class Service(db.Model):
	__tablename__ = 'service'
	#-------------- Columns ------------------#
	id_service = db.Column(db.Integer, primary_key=True, autoincrement=True)
	token_id = db.Column(db.String(50), unique=True, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
	client_id = db.Column(db.Integer, db.ForeignKey('client.id_client', ondelete='CASCADE'))
	vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id_vehicle', ondelete='CASCADE'))
	company_id = db.Column(db.Integer, db.ForeignKey('company.id_company', ondelete='RESTRICT'))
	operator_id = db.Column(db.Integer, db.ForeignKey('employee.id_employee', ondelete='RESTRICT'))
	resource_id = db.Column(db.Integer, db.ForeignKey('resource.id_resource', ondelete='CASCADE'))
	status_id = db.Column(db.Integer, db.ForeignKey('status.id_status', ondelete='CASCADE'))
	evidence_id = db.Column(db.Integer, db.ForeignKey('evidence.id_evidence', ondelete='CASCADE'))
	company_base_address = db.Column(db.String(255))
	service_cost = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.text('0'))
	tax = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.text('0'))
	service_date = db.Column(db.DateTime)
	start_time = db.Column(db.Time)
	end_time = db.Column(db.Time)
	service_duration = db.Column(db.Interval)
	observations = db.Column(db.Text)
	arrival_confirmation = db.Column(db.Boolean, server_default=db.text('FALSE'))
	completion_confirmation = db.Column(db.Boolean, server_default=db.text('FALSE'))
	rating_attention = db.Column(db.SmallInteger)
	rating_assistance = db.Column(db.SmallInteger)
	rating_system = db.Column(db.SmallInteger)
	service_type_id = db.Column(db.Integer, db.ForeignKey('servicetype.id_service_type', ondelete='RESTRICT'), nullable=False)
	#-------------- Constraints ------------------#
	__table_args__ = (
		db.CheckConstraint('LENGTH(token_id) = 50', name='chk_service_token_id_length'),
		db.CheckConstraint('service_cost >= 0', name='chk_service_cost_non_negative'),
		db.CheckConstraint('tax >= 0', name='chk_service_tax_non_negative'),
		db.CheckConstraint('(rating_attention BETWEEN 1 AND 5) OR rating_attention IS NULL', name='chk_service_rating_attention_range'),
		db.CheckConstraint('(rating_assistance BETWEEN 1 AND 5) OR rating_assistance IS NULL', name='chk_service_rating_assistance_range'),
		db.CheckConstraint('(rating_system BETWEEN 1 AND 5) OR rating_system IS NULL', name='chk_service_rating_system_range'),
		db.CheckConstraint("observations ~* '^[[:alnum:] .,;:!?()áéíóúÁÉÍÓÚñÑ-]*$'", name='chk_service_observations_charset'),
	)