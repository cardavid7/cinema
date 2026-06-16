from fastapi import APIRouter
from typing import List
from app.api.depends import DBSession
from app.models.movie import Movie, MovieCreate, MovieUpdate
from app.services.movie_service import MovieService

router = APIRouter(prefix='/movies', tags=['Movies'])

@router.get("/{movie_id}", response_model=Movie, status_code=200)
def get_movie_by_id(db: DBSession, movie_id: int):
    service = MovieService(db)
    return service.get_by_id(movie_id)

@router.get("/title/{movie_title}", response_model=List[Movie], status_code=200)
def get_movies_by_title(db: DBSession, movie_title: str):
    service = MovieService(db)
    return service.get_by_title(movie_title)
    
@router.post("/", response_model=Movie, status_code=201)
def create_movie(db: DBSession, movie: MovieCreate):
    service = MovieService(db)
    return service.create(movie)

@router.put("/{movie_id}", response_model=Movie, status_code=200)
def update_movie(db: DBSession, movie_id: int, movie: MovieUpdate):
    service = MovieService(db)
    return service.update(movie_id, movie)

@router.delete("/{movie_id}", status_code=204)
def delete_movie(db: DBSession, movie_id: int):
    service = MovieService(db)
    return service.delete(movie_id)
