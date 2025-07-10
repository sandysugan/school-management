from fastapi import APIRouter
from .endpoints import auth,users,academic,library,allocations,transport,fees,exams,timetable,attendance

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/login",tags=["Authentication"])
api_router.include_router(users.router,prefix="/user",tags=["Users"])
api_router.include_router(academic.router,prefix="/academic",tags=["Academics"])
api_router.include_router(attendance.router,prefix="/attendance",tags=["Attendance"])
api_router.include_router(exams.router,prefix="/exam",tags=["Examinations"])
api_router.include_router(allocations.router,prefix="/allocation",tags=["Allocations"])
api_router.include_router(transport.router,prefix="/transport",tags=["Transport"])
api_router.include_router(fees.router,prefix="/fees",tags=["Fees Management"])
api_router.include_router(timetable.router,prefix="/timetable",tags=["Time Table"])
api_router.include_router(library.router,prefix="/library",tags=["Library"])