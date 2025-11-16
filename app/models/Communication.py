from dataclasses import dataclass
from app.database import db

@dataclass
class Communication(db.Model):
	__tablename__ = 'communication'
	#-------------- Columns ------------------#
	id_communication = db.Column(db.Integer, primary_key=True, autoincrement=True)
	service_id = db.Column(db.Integer, db.ForeignKey('service.id_service'), nullable=False)
	sender_id = db.Column(db.Integer, db.ForeignKey('useraccount.id_user'), nullable=False)
	receiver_id = db.Column(db.Integer, db.ForeignKey('useraccount.id_user'), nullable=False)
	message = db.Column(db.Text)
	call = db.Column(db.Boolean, server_default=db.text('FALSE'))
	timestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())
	sender_role = db.Column(db.String(20))
	receiver_role = db.Column(db.String(20))
	#-------------- Constraints ------------------#
	__table_args__ = (
		db.CheckConstraint('service_id > 0 AND sender_id > 0 AND receiver_id > 0', name='chk_communication_ids_positive'),
		db.CheckConstraint('LENGTH(message) <= 250', name='chk_communication_message_length'),
		db.CheckConstraint("message ~* '^[A-Za-z0-9 .,;:!?()-\\n]*$'", name='chk_communication_message_charset'),
		db.CheckConstraint("sender_role IN ('client','employee')", name='chk_communication_sender_role'),
		db.CheckConstraint("receiver_role IN ('client','employee')", name='chk_communication_receiver_role'),
	)