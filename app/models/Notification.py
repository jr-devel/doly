from dataclasses import dataclass
from app.database import db

@dataclass
class Notification(db.Model):
	__tablename__ = 'notification'
	#-------------- Columns ------------------#
	id_notification = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('useraccount.id_user', ondelete='CASCADE'), nullable=False)
	message = db.Column(db.Text, nullable=False)
	read_status = db.Column(db.Boolean, server_default=db.text('FALSE'))
	created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
	#-------------- Constraints ------------------#
	__table_args__ = (
		db.CheckConstraint('LENGTH(message) <= 500', name='chk_notification_message_length'),
		db.CheckConstraint("message !~* '\\s{2,}'", name='chk_notification_message_whitespace'),
		db.CheckConstraint("message ~* '^[[:alnum:] .,;:!?()áéíóúÁÉÍÓÚñÑ-]*$'", name='chk_notification_message_charset'),
		db.CheckConstraint('user_id > 0', name='chk_notification_user_id_positive'),
	)