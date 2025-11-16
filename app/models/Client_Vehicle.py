from sqlalchemy import *
from sqlalchemy.orm import *
from app.database import db
from dataclasses import dataclass

###
# DROP TABLE IF EXISTS Client_Vehicle CASCADE;
# CREATE TABLE IF NOT EXISTS Client_Vehicle (
#     id_client_vehicle SERIAL PRIMARY KEY,
#     client_id INT NOT NULL,
#     vehicle_id INT NOT NULL,
#     CONSTRAINT fk_client_vehicle_client_id FOREIGN KEY (client_id) REFERENCES Client(id_client) ON DELETE CASCADE,
#     CONSTRAINT fk_client_vehicle_vehicle_id FOREIGN KEY (vehicle_id) REFERENCES Vehicle(id_vehicle) ON DELETE CASCADE,
#     CONSTRAINT uq_client_vehicle UNIQUE (client_id, vehicle_id),
#     CONSTRAINT chk_client_vehicle_id_positive CHECK (client_id > 0 AND vehicle_id > 0)
# );
###

@dataclass
class Client_Vehicle(db.Model):
    __tablename__ = 'client_vehicle'
    #-------------- Columns ------------------#
    id_client_vehicle = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, db.ForeignKey('client.id_client', ondelete='CASCADE'), nullable=False)
    vehicle_id = Column(Integer, db.ForeignKey('vehicle.id_vehicle', ondelete='CASCADE'), nullable=False)
    #-------------- Constraints ------------------#
    __table_args__ = (
        UniqueConstraint('client_id', 'vehicle_id', name='uq_client_vehicle'),
        CheckConstraint('client_id > 0 AND vehicle_id > 0', name='chk_client_vehicle_id_positive')
    )