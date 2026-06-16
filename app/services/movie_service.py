from sqlmodel import Session
from fastapi import HTTPException, status
from typing import List

from app.repositories.movie_repository import MovieRepository
from app.models.movie import Movie, MovieCreate, MovieUpdate

class MovieService:
    def __init__(self, db:Session):
        self.movie_repo = MovieRepository(db)

    def get_by_id(self, movie_id: int) -> Movie:
        movie = self.movie_repo.get_by_id(movie_id)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {movie_id} not found")
        return movie

    def get_by_title(self, title: str) -> List[Movie]:
        movies = self.movie_repo.get_by_title(title)
        if not movies:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movies with title '{title}' not found")
        return movies
    
    def create(self, movie_data: MovieCreate) -> Movie:
        existing_movie = self.movie_repo.get_by_title_and_format(movie_data.title, movie_data.format)
        if existing_movie:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Movie with title '{movie_data.title}' and format '{movie_data.format}' already exists")
        return self.movie_repo.create(movie_data)
    
    def update(self, movie_id: int, movie_data: MovieUpdate) -> Movie:
        movie = self.movie_repo.get_by_id(movie_id)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {movie_id} not found")
        
        new_title = movie_data.title if movie_data.title is not None else movie.title
        new_format = movie_data.format if movie_data.format is not None else movie.format

        if movie.title != new_title or movie.format != new_format:
            existing_movie = self.movie_repo.get_by_title_and_format(new_title, new_format)
            if existing_movie:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Movie with title '{new_title}' and format '{new_format}' already exists")
        
        movie.title = new_title
        movie.format = new_format
        movie.description = movie_data.description if movie_data.description is not None else movie.description
        movie.duration = movie_data.duration if movie_data.duration is not None else movie.duration
        return self.movie_repo.update(movie)
    
    def delete(self, movie_id: int) -> bool:
        movie = self.movie_repo.get_by_id(movie_id)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {movie_id} not found")
        self.movie_repo.delete(movie)
        return True