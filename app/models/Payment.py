from dataclasses import dataclass
from app.database import db

###
# Payment table per DDL
###

@dataclass
class Payment(db.Model):
	__tablename__ = 'payment'
	#-------------- Columns ------------------#
	id_payment = db.Column(db.Integer, primary_key=True, autoincrement=True)
	service_id = db.Column(db.Integer, db.ForeignKey('service.id_service', ondelete='CASCADE'), nullable=False)
	client_id = db.Column(db.Integer, db.ForeignKey('client.id_client', ondelete='CASCADE'), nullable=False)
	company_id = db.Column(db.Integer, db.ForeignKey('company.id_company', ondelete='CASCADE'), nullable=False)
	payment_method = db.Column(db.String(50), nullable=False)
	payment_status = db.Column(db.String(30), server_default=db.text("'pending'"))
	amount = db.Column(db.Numeric(10, 2), nullable=False)
	commission = db.Column(db.Numeric(10, 2), server_default=db.text('0'))
	total_transferred = db.Column(db.Numeric(10, 2), server_default=db.text('0'))
	payment_date = db.Column(db.DateTime, server_default=db.func.current_timestamp())
	#-------------- Constraints ------------------#
	__table_args__ = (
		db.CheckConstraint("payment_method IN ('credit_card','debit_card','transfer','cash')", name='chk_payment_method'),
		db.CheckConstraint("payment_status IN ('pending','confirmed','canceled','refunded','failed','in_process','on_hold','partially_refunded')", name='chk_payment_status'),
		db.CheckConstraint('amount >= 0', name='chk_payment_amount_non_negative'),
		db.CheckConstraint('commission >= 0', name='chk_payment_commission_non_negative'),
		db.CheckConstraint('total_transferred >= 0', name='chk_payment_total_transferred_non_negative'),
		db.CheckConstraint('service_id > 0', name='chk_payment_service_id_positive'),
		db.CheckConstraint('client_id > 0', name='chk_payment_client_id_positive'),
		db.CheckConstraint('company_id > 0', name='chk_payment_company_id_positive'),
	)