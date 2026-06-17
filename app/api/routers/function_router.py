
from fastapi import APIRouter

from app.models.function import Function, FunctionCreate, FunctionUpdate, FunctionRead
from app.api.depends import DBSession
from app.services.function_service import FunctionService

router = APIRouter(prefix='/functions', tags=['Functions'])

@router.get('/{function_id}', response_model=FunctionRead, status_code=200)
def get_function_by_id(db:DBSession, function_id: int):
    service = FunctionService(db)
    return service.get_by_id(function_id)

@router.get('/movie/{movie_id}', response_model=list[FunctionRead], status_code=200)
def get_all_by_movie_id(db:DBSession, movie_id: int):
    service = FunctionService(db)
    return service.get_all_by_movie_id(movie_id)

@router.get('/room/{room_id}', response_model=list[FunctionRead], status_code=200)
def get_all_by_room_id(db:DBSession, room_id: int):
    service = FunctionService(db)
    return service.get_all_by_room_id(room_id)

@router.post('/', response_model=FunctionRead, status_code=201)
def create_function(db:DBSession, function: FunctionCreate):
    service = FunctionService(db)
    return service.create(function)

@router.put('/{function_id}', response_model=FunctionRead, status_code=200)
def update_function(db:DBSession, function_id: int, function: FunctionUpdate):
    service = FunctionService(db)
    return service.update(function_id, function)

@router.delete('/{function_id}', status_code=204)
def delete_function(db:DBSession, function_id: int):
    service = FunctionService(db)
    return service.delete(function_id)