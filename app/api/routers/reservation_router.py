from fastapi import APIRouter

from app.models.reservation import ReservationCreate, ReservationUpdate, ReservationRead
from app.api.depends import DBSession, CurrentUser
from app.services.reservation_service import ReservationService

router = APIRouter(prefix='/reservations', tags=['Reservations'])

@router.get('/{reservation_id}', response_model=ReservationRead, status_code=200)
def get_reservation_by_id(db:DBSession, reservation_id: int, user: CurrentUser):
    service = ReservationService(db)
    return service.get_by_id(reservation_id)

@router.get('/user/{user_id}', response_model=list[ReservationRead], status_code=200)
def get_by_user_id(db:DBSession, user_id: int, user: CurrentUser):
    service = ReservationService(db)
    return service.get_by_user_id(user_id)

@router.get('/function/{function_id}', response_model=list[ReservationRead], status_code=200)
def get_by_function_id(db:DBSession, function_id: int, user: CurrentUser):
    service = ReservationService(db)
    return service.get_by_function_id(function_id)

@router.post('/', response_model=ReservationRead, status_code=201)
def create_reservation(db:DBSession, reservation: ReservationCreate, user: CurrentUser):
    service = ReservationService(db)
    return service.create(reservation, user.id)

@router.put('/{reservation_id}', response_model=ReservationRead, status_code=200)
def update_reservation(db:DBSession, reservation_id: int, reservation: ReservationUpdate, user: CurrentUser):
    service = ReservationService(db)
    return service.update(reservation_id, reservation)

@router.delete('/{reservation_id}', status_code=204)
def delete_reservation(db:DBSession, reservation_id: int, user: CurrentUser):
    service = ReservationService(db)
    return service.delete(reservation_id)
