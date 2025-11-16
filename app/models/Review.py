from dataclasses import dataclass
from app.database import db

@dataclass
class Review(db.Model):
	__tablename__ = 'review'
	#-------------- Columns ------------------#
	id_review = db.Column(db.Integer, primary_key=True, autoincrement=True)
	service_id = db.Column(db.Integer, db.ForeignKey('service.id_service', ondelete='CASCADE'), nullable=False)
	reviewer_id = db.Column(db.Integer, nullable=False)
	review_type = db.Column(db.String(30))
	rating = db.Column(db.SmallInteger)
	comment = db.Column(db.Text)
	review_date = db.Column(db.DateTime, server_default=db.func.current_timestamp())
	#-------------- Constraints ------------------#
	__table_args__ = (
		db.CheckConstraint('service_id > 0', name='chk_review_service_id_positive'),
		db.CheckConstraint('reviewer_id > 0', name='chk_review_reviewer_id_positive'),
		db.CheckConstraint("review_type IN ('client_to_provider','provider_to_client')", name='chk_review_type_allowed'),
		db.CheckConstraint("review_type IS NOT NULL AND review_type <> ''", name='chk_review_type_not_empty'),
		db.CheckConstraint('comment IS NULL OR LENGTH(comment) <= 1000', name='chk_review_comment_length'),
		db.CheckConstraint("comment IS NULL OR comment !~* '\\s{2,}'", name='chk_review_comment_whitespace'),
		db.CheckConstraint("comment IS NULL OR comment ~* '^[A-Za-z0-9 .,;:!?()-\\n]*$'", name='chk_review_comment_charset'),
		db.CheckConstraint('review_date <= CURRENT_TIMESTAMP', name='chk_review_date_past'),
		db.CheckConstraint('rating IS NULL OR rating BETWEEN 0 AND 5', name='chk_review_rating_range'),
	)