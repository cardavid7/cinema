from sqlmodel import Session, select
from app.models.movie import Movie

class MovieRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, movie_id: int) -> Movie | None:
        return self.db.get(Movie, movie_id)

    def get_by_title(self, title: str) -> Movie | None:
        return self.db.exec(select(Movie).where(Movie.title == title)).first()

    def get_by_title_and_format(self, title: str, format: str) -> Movie | None:
        return self.db.exec(select(Movie).where(Movie.title == title, Movie.format == format)).first()
    
    def create(self, movie: Movie):
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie
    
    def update(self, movie: Movie):
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie
    
    def delete(self, movie: Movie):
        self.db.delete(movie)
        self.db.commit()