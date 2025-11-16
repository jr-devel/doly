from dataclasses import dataclass
from app.database import db

# AuditLog table per DDL

@dataclass
class AuditLog(db.Model):
    __tablename__ = 'auditLog'
    #-------------- Columns ------------------#
    id_audit = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('useraccount.id_user', ondelete='RESTRICT'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    table_name = db.Column(db.String(50), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    old_value = db.Column(db.JSON)
    new_value = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('LENGTH(action) <= 100', name='chk_audit_action_length'),
        db.CheckConstraint('LENGTH(table_name) <= 50', name='chk_audit_table_name_length'),
        db.CheckConstraint('user_id > 0', name='chk_audit_user_id_positive'),
        db.CheckConstraint('record_id > 0', name='chk_audit_record_id_positive'),
        db.CheckConstraint("action !~* '\\s{2,}'", name='chk_audit_action_no_whitespace'),
        db.CheckConstraint("table_name !~* '\\s'", name='chk_audit_table_name_no_whitespace'),
        db.CheckConstraint("action ~* '^[A-Za-z0-9_ ]+$'", name='chk_audit_action_format'),
        db.CheckConstraint("table_name ~* '^[A-Za-z0-9_]+$'", name='chk_audit_table_name_format'),
        db.CheckConstraint('(old_value IS DISTINCT FROM new_value OR new_value IS NULL)', name='chk_audit_newvalue_differs_oldvalue'),
    )
