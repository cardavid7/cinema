
from fastapi import APIRouter

from app.services.user_service import UserService
from app.models.user import User, UserCreate, UserUpdate
from app.api.depends import DBSession

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}", response_model=User, status_code=200)
def get_user_by_id(user_id: int, db: DBSession):
    return UserService(db).get_by_id(user_id)

@router.post("/", response_model=User, status_code=201)
def create_user(user: UserCreate, db: DBSession):
    return UserService(db).create(user)

@router.put("/{user_id}", response_model=User, status_code=200)
def update_user(user_id: int, user: UserUpdate, db: DBSession):
    return UserService(db).update(user_id, user)

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: DBSession):
    return UserService(db).delete(user_id)