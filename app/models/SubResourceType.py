from sqlalchemy import *
from sqlalchemy.orm import *
from app.database import db
from dataclasses import dataclass

###
# DROP TABLE IF EXISTS SubResourceType CASCADE;
# CREATE TABLE IF NOT EXISTS SubResourceType (
#     id_sub_resource_type SERIAL PRIMARY KEY,
#     name VARCHAR(50) NOT NULL,
#     resource_type_id INT NOT NULL,
#     CONSTRAINT fk_subresource_type_resource_type_id FOREIGN KEY (resource_type_id) REFERENCES ResourceType(id_resource_type) ON DELETE CASCADE,
#     CONSTRAINT chk_subresource_type_name CHECK (LENGTH(name) >= 3 AND LENGTH(name) <= 50)
# );
###

@dataclass
class SubResourceType(db.Model):
    __tablename__ = "subresourcetype"
    #-------------- Columns ------------------#
    id_sub_resource_type = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    resource_type_id = db.Column(db.Integer, db.ForeignKey('resourcetype.id_resource_type', ondelete='CASCADE'), nullable=False)
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('LENGTH(name) >= 3 AND LENGTH(name) <= 50', name='chk_subresource_type_name'),
    )