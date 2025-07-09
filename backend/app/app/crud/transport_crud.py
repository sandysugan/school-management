from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.models import Driver,Bus,StudentTransport
from app.schemas import DriverSchema,BusSchema,StudentTransportSchema

#-----------------------------------CRUD for drivers--------------------------------------------------#

def create_bulk_drivers(db: Session, driver_data: List[DriverSchema]):
    now = datetime.utcnow()
    driver_objs = [
        Driver(
            name=d.name,
            license_number=d.license_number,
            phone_number=d.phone_number,
            status=d.status,
            created_by=d.created_by,
            updated_by=d.updated_by,
            created_at=now,
            updated_at=now
        )
        for d in driver_data
    ]
    db.add_all(driver_objs)
    db.commit()
    return driver_objs

def update_bulk_drivers(db: Session, updates:DriverSchema ):
    now = datetime.utcnow()
    updated_records = []

    for upd in updates:
        db_obj = db.query(Driver).filter(Driver.id == upd.id).first()
        if db_obj:
            for field, value in upd.dict(exclude_unset=True, exclude={"id"}).items():
                setattr(db_obj, field, value)
            db_obj.updated_at = now
            db.commit()
            db.refresh(db_obj)
            updated_records.append(db_obj)

    return updated_records

def get_all_drivers(db: Session):
    return db.query(Driver).filter(Driver.status == 1).all()

def get_driver_by_id(db: Session, id: int):
    return db.query(Driver).filter(Driver.id == id).first()

def soft_delete_driver(db: Session, id: int, updated_by: int):
    db_obj = db.query(Driver).filter(Driver.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False

#-----------------------------------CRUD for buses-------------------------------------------#

def create_bulk_buses(db: Session, buses_data: list[BusSchema]):
    now = datetime.utcnow()
    bus_objs = []

    for data in buses_data:
        bus = Bus(
            bus_number=data.bus_number,
            driver_id=data.driver_id,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now,
        )
        bus_objs.append(bus)

    db.add_all(bus_objs)
    db.commit()
    return bus_objs

def get_all_buses(db: Session):
    return db.query(Bus).filter(Bus.status == 1).all()

def get_bus_by_id(db: Session, id: int):
    return db.query(Bus).filter(Bus.id == id).first()

def update_bus(db: Session, id: int, data: BusSchema):
    db_obj = db.query(Bus).filter(Bus.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_bus(db: Session, id: int, updated_by: int):
    db_obj = db.query(Bus).filter(Bus.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False

#-------------------------------------------CRUD for student_transport-----------------------------------------------#


def create_bulk_transports(db: Session, transports_data: list[StudentTransportSchema]):
    now = datetime.utcnow()
    transport_objs = []

    for data in transports_data:
        transport = StudentTransport(
            student_id=data.student_id,
            bus_id=data.bus_id,
            pickup_point=data.pickup_point,
            drop_point=data.drop_point,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now
        )
        transport_objs.append(transport)

    db.add_all(transport_objs)
    db.commit()
    return transport_objs

def get_all_transports(db: Session):
    return db.query(StudentTransport).filter(StudentTransport.status == 1).all()

def get_transport_by_id(db: Session, id: int):
    return db.query(StudentTransport).filter(StudentTransport.id == id).first()

def update_transport(db: Session, id: int, data: StudentTransportSchema):
    db_obj = db.query(StudentTransport).filter(StudentTransport.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_transport(db: Session, id: int, updated_by: int):
    db_obj = db.query(StudentTransport).filter(StudentTransport.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False