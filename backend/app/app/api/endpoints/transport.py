from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models import User
from app.schemas import BulkDriverSchema,DriverSchema,BusSchema,BulkBusSchema,StudentTransportSchema,BulkStudentTransportSchema
from app.crud import transport_crud

router = APIRouter()

#---------------------------------------api for drivers-------------------------------------------#

@router.post("/bulk_driver_create/")
def bulk_create_drivers(
    data: BulkDriverSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type !=1:
         return {"status":0, "detail":"Unauthorized User"}

    for driver in data.drivers:
        driver.created_by = current_user.id
        driver.updated_by = current_user.id

    created = transport_crud.create_bulk_drivers(db, data.drivers)

    return {
        "status": 1,
        "msg": f"{len(created)} drivers created successfully",
        "data": [{"id": d.id, "name": d.name, "license": d.license_number} for d in created]
    }

@router.post("/driver_update/")
def bulk_update_drivers(
    data:DriverSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type !=1:
         return {"status":0, "detail":"Unauthorized User"}

    for d in data.updates:
        d.updated_by = current_user.id

    updated = transport_crud.update_bulk_drivers(db, data.updates)

    return {
        "status": 1,
        "msg": f"{len(updated)} drivers updated successfully",
        "data": [{"id": d.id, "name": d.name} for d in updated]
    }

@router.post("/list_drivers/")
def list_drivers(skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}
    
    drivers = transport_crud.get_all_drivers(db)[skip:skip + limit]
    return [{"id": d.id, "name": d.name, "license": d.license_number, "phone": d.phone_number} for d in drivers]

@router.post("/get_driver/{id}")
def get_driver(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    driver =transport_crud.get_driver_by_id(db, id)
    if not driver or driver.status != 1:
        return {"status":0,"detail":"Driver not found"}

    return {
        "id": driver.id,
        "name": driver.name,
        "license": driver.license_number,
        "phone": driver.phone_number
    }

@router.post("/delete_driver/{id}")
def delete_driver(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type !=1:
         return {"status":0, "detail":"Unauthorized User"}

    success = transport_crud.soft_delete_driver(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Driver not found"}
    
    return {"status": 1, "msg": "Driver deleted successfully"}

#-----------------------------api for buses--------------------------------------#


@router.post("/bulk_bus_create")
def bulk_create_buses(
    data: BulkBusSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type !=1:
         return {"status":0, "detail":"Unauthorized User"}
    
    for bus in data.buses:
        bus.created_by = current_user.id
        bus.updated_by = current_user.id

    created_buses = transport_crud.create_bulk_buses(db, data.buses)
    result = [
        {
            "bus_id": bus.id,
            "bus_number": bus.bus_number,
            "driver_id": bus.driver_id,
            "status": bus.status,
            "created_by": bus.created_by
        }
        for bus in created_buses
    ]

    return {
        "status": 1,
        "msg": f"{len(result)} buses created successfully",
        "data": result
    }

@router.post("/list_all_buses/")
def list_buses(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}
    
    buses = transport_crud.get_all_buses(db)[skip: skip + limit]
    return [
        {
            "bus_id": bus.id,
            "bus_number": bus.bus_number,
            "driver_id": bus.driver_id,
            "status": bus.status,
            "created_by": bus.created_by
        }
        for bus in buses
    ]

@router.post("/get_bus/{id}")
def get_bus(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}
    
    bus = transport_crud.get_bus_by_id(db, id)
    if not bus or bus.status != 1:
        return {"status":0,"detail":"Bus not found"}
    
    return {
        "bus_id": bus.id,
        "bus_number": bus.bus_number,
        "driver_id": bus.driver_id,
        "status": bus.status,
        "created_by": bus.created_by,
        "updated_by": bus.updated_by
    }

@router.post("/update_bus/{id}")
def update_bus(
    id: int,
    data: BusSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type!=1:
         return {"status":0, "detail":"Unauthorized User"}
    
    data.updated_by = current_user.id
    updated = transport_crud.update_bus(db, id, data)
    if not updated:
        return {"status":0,"detail":"Bus not found"}

    return {
        "msg": "Bus updated successfully",
        "bus_id": updated.id,
        "updated_by": updated.updated_by
    }

@router.post("/delete_bus/{id}")
def delete_bus(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type!=1:
         return {"status":0, "detail":"Unauthorized User"}
    
    success = transport_crud.soft_delete_bus(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Bus not found"}

    return {
        "status": 1,
        "msg": "Bus deleted successfully"
    }

#------------------------------------------api for student_transport---------------------------------------------------#

@router.post("/bulk_student_transport_create")
def bulk_create_student_transports(
    data: BulkStudentTransportSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    for transport in data.transports:
        transport.created_by = current_user.id
        transport.updated_by = current_user.id

    created_transports = transport_crud.create_bulk_transports(db, data.transports)
    result = [
        {
            "id": t.id,
            "student_id": t.student_id,
            "bus_id": t.bus_id,
            "pickup_point": t.pickup_point,
            "drop_point": t.drop_point,
            "status": t.status
        }
        for t in created_transports
    ]

    return {
        "status": 1,
        "msg": f"{len(result)} records created successfully",
        "data": result
    }

@router.post("/list_student_transport/")
def list_student_transports(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,5]:
         return {"status":0, "detail":"Unauthorized User"}

    transports = transport_crud.get_all_transports(db)[skip: skip + limit]
    return [
        {
            "id": t.id,
            "student_id": t.student_id,
            "bus_id": t.bus_id,
            "pickup_point": t.pickup_point,
            "drop_point": t.drop_point,
            "status": t.status
        }
        for t in transports
    ]

@router.post("/get_student_transport/{id}")
def get_student_transport(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,4,5]:
         return {"status":0, "detail":"Unauthorized User"}

    transport = transport_crud.get_transport_by_id(db, id)
    if not transport or transport.status != 1:
        return {"status":0,"detail":"Student transport record not found"}

    return {
        "id": transport.id,
        "student_id": transport.student_id,
        "bus_id": transport.bus_id,
        "pickup_point": transport.pickup_point,
        "drop_point": transport.drop_point,
        "status": transport.status,
        "created_by": transport.created_by,
        "updated_by": transport.updated_by
    }

@router.post("/update_student_transport/{id}")
def update_student_transport(
    id: int,
    data: StudentTransportSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    data.updated_by = current_user.id
    updated =transport_crud.update_transport(db, id, data)
    if not updated:
        return {"status":0,"detail":"Student transport record not found"}

    return {
        "msg": "Student transport record updated successfully",
        "id": updated.id,
        "updated_by": updated.updated_by
    }

@router.post("/delete_student_transport/{id}")
def delete_student_transport(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    success = transport_crud.soft_delete_transport(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Student transport record not found"}

    return {
        "status": 1,
        "msg": "Student transport record deleted successfully"
    }