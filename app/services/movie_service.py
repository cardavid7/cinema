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
        existing_movie = self.movie_repo.get_by_title_and_format(movie.title, movie.format)
        if existing_movie:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Movie with title '{movie.title}' and format '{movie.format}' already exists")
        return self.movie_repo.create(movie)
    
    def update(self, movie_id: int, movie_data: Movie) -> Movie:
        movie = self.movie_repo.get_by_id(movie_id)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {movie.id} not found")
        
        if movie.title != movie_data.title or movie.format != movie_data.format:
            existing_movie = self.movie_repo.get_by_title_and_format(movie_data.title, movie_data.format)
            if existing_movie:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Movie with title '{movie_data.title}' and format '{movie_data.format}' already exists")
        
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