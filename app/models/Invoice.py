from dataclasses import dataclass
from app.database import db

@dataclass
class Invoice(db.Model):
	__tablename__ = 'invoice'
	#-------------- Columns ------------------#
	id_invoice = db.Column(db.Integer, primary_key=True, autoincrement=True)
	payment_id = db.Column(db.Integer, db.ForeignKey('payment.id_payment', ondelete='CASCADE'), nullable=False)
	client_id = db.Column(db.Integer, db.ForeignKey('client.id_client', ondelete='CASCADE'), nullable=False)
	rfc = db.Column(db.String(20), nullable=False)
	business_name = db.Column(db.String(100))
	fiscal_address = db.Column(db.String(255))
	total = db.Column(db.Numeric(10, 2), nullable=False)
	issue_date = db.Column(db.DateTime, server_default=db.func.current_timestamp())
	pdf_path = db.Column(db.String(255))
	#-------------- Constraints ------------------#
	__table_args__ = (
		db.CheckConstraint('LENGTH(rfc) BETWEEN 12 AND 20', name='chk_invoice_rfc_length'),
		db.CheckConstraint("rfc ~* '^[A-Za-z0-9]+$'", name='regex_invoice_rfc_format'),
		db.CheckConstraint('business_name IS NULL OR LENGTH(business_name) <= 100', name='chk_invoice_business_name_length'),
		db.CheckConstraint("business_name IS NULL OR business_name !~* '\\s{2,}'", name='regex_invoice_business_name_whitespace'),
		db.CheckConstraint("business_name IS NULL OR business_name ~* '^[A-Za-z0-9 .,;:!?()-]*$'", name='regex_invoice_business_name_charset'),
		db.CheckConstraint('fiscal_address IS NULL OR LENGTH(fiscal_address) <= 255', name='chk_invoice_fiscal_address_length'),
		db.CheckConstraint("fiscal_address IS NULL OR fiscal_address !~* '\\s{2,}'", name='regex_invoice_fiscal_address_whitespace'),
		db.CheckConstraint("fiscal_address IS NULL OR fiscal_address ~* '^[A-Za-z0-9 .,;:!?()-]*$'", name='regex_invoice_fiscal_address_charset'),
		db.CheckConstraint('pdf_path IS NULL OR LENGTH(pdf_path) <= 255', name='chk_invoice_pdf_path_length'),
		db.CheckConstraint("pdf_path IS NULL OR pdf_path !~* '\\s'", name='regex_invoice_pdf_path_no_whitespace'),
		db.CheckConstraint('total >= 0', name='chk_invoice_total_non_negative'),
		db.CheckConstraint('payment_id > 0', name='chk_invoice_payment_id_positive'),
		db.CheckConstraint('client_id > 0', name='chk_invoice_client_id_positive'),
		db.CheckConstraint('issue_date <= CURRENT_TIMESTAMP', name='chk_invoice_issue_date_past'),
	)