from dataclasses import dataclass
from app.database import db

###
# DROP TABLE IF EXISTS Resource CASCADE;
# CREATE TABLE IF NOT EXISTS Resource (
#     id_resource SERIAL PRIMARY KEY,
#     economic_code VARCHAR(20) UNIQUE NOT NULL,
#     resource_type_id INT NOT NULL,
#     sub_resource_type_id INT NOT NULL,
#     last_maintenance DATE,
#     CONSTRAINT fk_resource_type_id FOREIGN KEY (resource_type_id) REFERENCES ResourceType(id_resource_type),
#     CONSTRAINT fk_sub_resource_type_id FOREIGN KEY (sub_resource_type_id) REFERENCES SubResourceType(id_sub_resource_type),
#     CONSTRAINT chk_resource_economic_code CHECK (LENGTH(economic_code) >= 3 AND LENGTH(economic_code) <= 20),
#     CONSTRAINT chk_resource_type_id CHECK (resource_type_id > 0),
#     CONSTRAINT chk_sub_resource_type_id CHECK (sub_resource_type_id > 0),
#     CONSTRAINT chk_resource_last_maintenance CHECK (last_maintenance <= CURRENT_DATE),
#     CONSTRAINT chk_resource_economic_code_no_whitespace CHECK (economic_code !~* '\s'),
#     CONSTRAINT regex_resource_economic_code_format CHECK (economic_code ~* '^[A-Za-z0-9-]+$')
# );
###

@dataclass
class Resource(db.Model):
    __tablename__ = "resource"
    #-------------- Columns ------------------#
    id_resource = db.Column(db.Integer, primary_key=True, autoincrement=True)
    economic_code = db.Column(db.String(20), unique=True, nullable=False)
    resource_type_id = db.Column(db.Integer, db.ForeignKey('resourcetype.id_resource_type'), nullable=False)
    sub_resource_type_id = db.Column(db.Integer, db.ForeignKey('subresourcetype.id_sub_resource_type'), nullable=False)
    last_maintenance = db.Column(db.Date)
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('LENGTH(economic_code) >= 3 AND LENGTH(economic_code) <= 20', name='chk_resource_economic_code'),
        db.CheckConstraint('resource_type_id > 0', name='chk_resource_type_id'),
        db.CheckConstraint('sub_resource_type_id > 0', name='chk_sub_resource_type_id'),
        db.CheckConstraint('last_maintenance <= CURRENT_DATE', name='chk_resource_last_maintenance'),
        db.CheckConstraint("economic_code !~* '\\s'", name='chk_resource_economic_code_no_whitespace'),
        db.CheckConstraint("economic_code ~* '^[A-Za-z0-9-]+$'", name='regex_resource_economic_code_format'),
    )