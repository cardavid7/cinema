from sqlmodel import Session, select
from app.core.db import init_db, engine
from app.models.movie import Movie


def seed_movie():
    # Starting database table creation
    init_db()

    # Initial data for movie
    movies_data = [
        {"title": "Captain America: The First Avenger", "description": "A superhero film based on the Marvel Comics character Captain America. It is the fifth film in the Marvel Cinematic Universe (MCU).", "duration": 124, "format": "2D"},
        {"title": "Iron Man", "description": "Tony Stark, a wealthy American industrialist and genius inventor, is kidnapped and forced to build an armored suit to save his own life.", "duration": 126, "format": "2D_SUB"},
        {"title": "Thor: Ragnarok", "description": "Thor teams up with the Hulk and Valkyrie to save Asgard from Hela.", "duration": 130, "format": "2D_SUB"},
        {"title": "Avengers: Infinity War", "description": "The Avengers and their allies must put everything on the line to take down the powerful Thanos.", "duration": 149, "format": "3D"},
        {"title": "Captain Marvel", "description": "Carol Danvers becomes one of the most powerful heroes in the universe when Earth is caught in the middle of a galactic war.", "duration": 124, "format": "3D_SUB"},
    ]

    print("Starting seed of movies...")

    with Session(engine) as session:
        for m_data in movies_data:
            statement = select(Movie).where(Movie.title == m_data["title"], Movie.format == m_data["format"])
            existing_movie = session.exec(statement).first()

            if not existing_movie:
                movie = Movie(title=m_data["title"], description=m_data["description"], duration=m_data["duration"], format=m_data["format"])
                session.add(movie)
                print(f"-----> Creating movie: {m_data['title']}, Format: {m_data['format']}")
            else:
                print(f"-----> Movie '{m_data['title']}' already exists. Skipping.")
        
        session.commit()
    print("Seed of movies completed successfully!")

if __name__ == "__main__":
    seed_movie()