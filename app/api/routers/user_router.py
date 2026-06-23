
from fastapi import APIRouter

from app.services.user_service import UserService
from app.models.user import UserCreate, UserUpdate, UserRead
from app.api.depends import DBSession, CurrentUser

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}", response_model=UserRead, status_code=200)
def get_user_by_id(user_id: int, db: DBSession, user: CurrentUser):
    return UserService(db).get_by_id(user_id)

@router.post("/", response_model=UserRead, status_code=201)
def create_user(user_data: UserCreate, db: DBSession, user: CurrentUser):
    return UserService(db).create(user_data)

@router.put("/{user_id}", response_model=UserRead, status_code=200)
def update_user(user_id: int, user_data: UserUpdate, db: DBSession, user: CurrentUser):
    return UserService(db).update(user_id, user_data)

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: DBSession, user: CurrentUser):
    return UserService(db).delete(user_id)