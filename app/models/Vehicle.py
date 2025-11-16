from dataclasses import dataclass
from app.database import db

###
# DROP TABLE IF EXISTS Vehicle CASCADE;
# CREATE TABLE IF NOT EXISTS Vehicle (
#     id_vehicle SERIAL PRIMARY KEY,
#     vin VARCHAR(17) UNIQUE NOT NULL,
#     circulation_card VARCHAR(20),
#     brand VARCHAR(50),
#     plate VARCHAR(10),
#     model VARCHAR(50),
#     color VARCHAR(30),
#     vehicle_type_id INT NOT NULL, --TABLA FK
#     manufacturer VARCHAR(50),
#     insurer VARCHAR(50),
#     subbrand VARCHAR(50),
#     engine_serial VARCHAR(50),
#     mileage INT,
#     spare_tire BOOLEAN,
#     FOREIGN KEY (vehicle_type_id) REFERENCES VehicleType(id_vehicle_type) ON DELETE SET NULL,
#     CONSTRAINT chk_vehicle_vin_length CHECK (char_length(vin) = 17),
#     CONSTRAINT chk_vehicle_circulation_card_length CHECK (char_length(circulation_card) <= 20),
#     CONSTRAINT chk_vehicle_plate_length CHECK (char_length(plate) <= 10),
#     CONSTRAINT chk_vehicle_model_length CHECK (char_length(model) <= 50),
#     CONSTRAINT chk_vehicle_color_length CHECK (char_length(color) <= 30),
#     CONSTRAINT chk_vehicle_manufacturer_length CHECK (char_length(manufacturer) <= 50),
#     CONSTRAINT chk_vehicle_insurer_length CHECK (char_length(insurer) <= 50),
#     CONSTRAINT chk_vehicle_subbrand_length CHECK (char_length(subbrand) <= 50),
#     CONSTRAINT chk_vehicle_brand_length CHECK (char_length(brand) <= 50),
#     CONSTRAINT chk_vehicle_engine_serial_length CHECK (char_length(engine_serial) <= 50),
#     CONSTRAINT chk_vehicle_mileage_non_negative CHECK (mileage >= 0),
#     CONSTRAINT chk_vehicle_type_positive CHECK (type_id > 0),
#     CONSTRAINT regex_vehicle_vin_no_whitespace CHECK (vin !~* '\s'),
#     CONSTRAINT regex_vehicle_plate_no_whitespace CHECK (plate !~* '\s'),
#     CONSTRAINT regex_vehicle_engine_serial_no_whitespace CHECK (engine_serial !~* '\s'),
#     CONSTRAINT regex_vehicle_vin_format CHECK (vin ~* '^[A-HJ-NPR-Z0-9]{17}$'),
#     CONSTRAINT regex_vehicle_plate_format CHECK (plate ~* '^[A-HJ-NPR-Z0-9]+$'),
#     CONSTRAINT regex_vehicle_engine_serial_format CHECK (engine_serial ~* '^[A-HJ-NPR-Z0-9]+$')
# );
###

@dataclass
class Vehicle(db.Model):
    __tablename__ = "vehicle"
    #-------------- Columns ------------------#
    id_vehicle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vin = db.Column(db.String(17), unique=True, nullable=False)
    circulation_card = db.Column(db.String(20))
    brand = db.Column(db.String(50)) # TOYOTA, HONDA, FORD, CHEVROLET, NISSAN, ETC.
    plate = db.Column(db.String(10))
    model = db.Column(db.String(50)) # Year model
    color = db.Column(db.String(30))
    vehicle_type_id = db.Column(db.Integer, db.ForeignKey("vehicletype.id_vehicle_type", ondelete="CASCADE"), nullable=False)
    manufacturer = db.Column(db.String(50))
    insurer = db.Column(db.String(50)) # SEGURO GNP, MAPFRE, AXA, CHUBB, ETC.
    subbrand = db.Column(db.String(50)) # CELICA, COROLLA, CIVIC, ACCORD, ETC.
    engine_serial = db.Column(db.String(50))
    mileage = db.Column(db.Integer)
    spare_tire = db.Column(db.Boolean)
    #-------------- Constraints ------------------#
    __table_args__ = (
        db.CheckConstraint('char_length(vin) = 17', name='chk_vehicle_vin_length'),
        db.CheckConstraint('char_length(circulation_card) <= 20', name='chk_vehicle_circulation_card_length'),
        db.CheckConstraint('char_length(plate) <= 10', name='chk_vehicle_plate_length'),
        db.CheckConstraint('char_length(model) <= 50', name='chk_vehicle_model_length'),
        db.CheckConstraint('char_length(color) <= 30', name='chk_vehicle_color_length'),
        db.CheckConstraint('char_length(manufacturer) <= 50', name='chk_vehicle_manufacturer_length'),
        db.CheckConstraint('char_length(insurer) <= 50', name='chk_vehicle_insurer_length'),
        db.CheckConstraint('char_length(subbrand) <= 50', name='chk_vehicle_subbrand_length'),
        db.CheckConstraint('char_length(brand) <= 50', name='chk_vehicle_brand_length'),
        db.CheckConstraint('char_length(engine_serial) <= 50', name='chk_vehicle_engine_serial_length'),
        db.CheckConstraint('mileage >= 0', name='chk_vehicle_mileage_non_negative'),
        db.CheckConstraint('vehicle_type_id > 0', name='chk_vehicle_type_positive'),
        db.CheckConstraint("vin !~* '\\s'", name='regex_vehicle_vin_no_whitespace'),
        db.CheckConstraint("plate !~* '\\s'", name='regex_vehicle_plate_no_whitespace'),
        db.CheckConstraint("engine_serial !~* '\\s'", name='regex_vehicle_engine_serial_no_whitespace'),
        db.CheckConstraint("vin ~* '^[A-HJ-NPR-Z0-9]{17}$'", name='regex_vehicle_vin_format'),
        db.CheckConstraint("plate ~* '^[A-HJ-NPR-Z0-9]+$'", name='regex_vehicle_plate_format'),
        db.CheckConstraint("engine_serial ~* '^[A-HJ-NPR-Z0-9]+$'", name='regex_vehicle_engine_serial_format')
    )