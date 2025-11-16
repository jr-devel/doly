from sqlalchemy import *
from sqlalchemy.orm import *
from app.database import db
from dataclasses import dataclass

###
# DROP TABLE IF EXISTS VehicleType CASCADE;
# CREATE TABLE IF NOT EXISTS VehicleType (
#     id_vehicle_type SERIAL PRIMARY KEY,
#     name VARCHAR(50) NOT NULL,
#     CONSTRAINT chk_vehicle_type_name CHECK (LENGTH(name) >= 3 AND LENGTH(name) <= 50)
# ); -- SEDAN, PICKUP, SEDAN, SUV, TRUCK, VAN, MOTORCYCLE
###

@dataclass
class VehicleType(db.Model):
    __tablename__ = "vehicletype"
    #-------------- Columns ------------------#
    id_vehicle_type = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('LENGTH(name) >= 3 AND LENGTH(name) <= 50', name='chk_vehicle_type_name'),
    )