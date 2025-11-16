from dataclasses import dataclass
from app.database import db

# ClientType table per DDL

@dataclass
class ClientType(db.Model):
    __tablename__ = 'clienttype'
    #-------------- Columns ------------------#
    id_client_type = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('LENGTH(name) >= 3 AND LENGTH(name) <= 50', name='chk_client_type_name'),
    )
