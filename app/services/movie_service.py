from sqlmodel import Session
from fastapi import HTTPException, status

from app.repositories.movie_repository import MovieRepository
from app.models.movie import Movie

class MovieService:
    def __init__(self, db:Session):
        self.movie_repo = MovieRepository(db)

    def get_by_id(self, movie_id: int) -> Movie:
        movie = self.movie_repo.get_by_id(movie_id)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {movie_id} not found")
        return movie

    def get_by_title(self, title: str) -> Movie:
        movie = self.movie_repo.get_by_title(title)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with title '{title}' not found")
        return movie
    
    def create(self, movie: Movie) -> Movie:
        return self.movie_repo.create(movie)
    
    def update(self, movie_id: int, movie_data: Movie) -> Movie:
        movie = self.movie_repo.get_by_id(movie_id)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {movie.id} not found")
        movie.title = movie_data.title
        movie.duration = movie_data.duration
        movie.rating = movie_data.rating
        return self.movie_repo.update(movie)
    
    def delete(self, movie_id: int) -> bool:
        movie = self.movie_repo.get_by_id(movie_id)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {movie_id} not found")
        self.movie_repo.delete(movie)
        return True