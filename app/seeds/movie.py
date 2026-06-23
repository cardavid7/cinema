from sqlmodel import Session, select
from app.core.db import init_db, engine
from app.models.movie import Movie, MovieCreate, MovieFormat
from app.services.movie_service import MovieService
from fastapi import HTTPException

def seed_movie():
    init_db()

    movies_data = [
        # Original 5 movies
        MovieCreate(
            title="Captain America: The First Avenger", 
            description="A superhero film based on the Marvel Comics character Captain America. It is the fifth film in the Marvel Cinematic Universe (MCU).", 
            duration=124, 
            format=MovieFormat.TWO_D
        ),
        MovieCreate(
            title="Iron Man", 
            description="Tony Stark, a wealthy American industrialist and genius inventor, is kidnapped and forced to build an armored suit to save his own life.", 
            duration=126, 
            format=MovieFormat.TWO_D_SUB
        ),
        MovieCreate(
            title="Thor: Ragnarok", 
            description="Thor teams up with the Hulk and Valkyrie to save Asgard from Hela.", 
            duration=130, 
            format=MovieFormat.TWO_D_SUB
        ),
        MovieCreate(
            title="Avengers: Infinity War", 
            description="The Avengers and their allies must put everything on the line to take down the powerful Thanos.", 
            duration=149, 
            format=MovieFormat.THREE_D
        ),
        MovieCreate(
            title="Captain Marvel", 
            description="Carol Danvers becomes one of the most powerful heroes in the universe when Earth is caught in the middle of a galactic war.", 
            duration=124, 
            format=MovieFormat.THREE_D_SUB
        ),
        # New 5 movies
        MovieCreate(
            title="The Dark Knight",
            description="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
            duration=152,
            format=MovieFormat.TWO_D
        ),
        MovieCreate(
            title="Inception",
            description="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
            duration=148,
            format=MovieFormat.TWO_D_SUB
        ),
        MovieCreate(
            title="Avatar: The Way of Water",
            description="Jake Sully lives with his newfound family formed on the extraterrestrial planet of Pandora. Once a familiar threat returns, Jake must work with Neytiri and the army of the Na'vi race to protect their home.",
            duration=192,
            format=MovieFormat.THREE_D
        ),
        MovieCreate(
            title="Spider-Man: Into the Spider-Verse",
            description="Teen Miles Morales becomes the Spider-Man of his universe, and must join with five spider-powered individuals from other dimensions to stop a threat for all realities.",
            duration=117,
            format=MovieFormat.TWO_D
        ),
        MovieCreate(
            title="Interstellar",
            description="When Earth becomes uninhabitable, a team of explorers travels through a wormhole in space in an attempt to ensure humanity's survival.",
            duration=169,
            format=MovieFormat.TWO_D_SUB
        ),
    ]

    print("Starting seed of movies...")

    with Session(engine) as session:
        movie_service = MovieService(session)
        for m_data in movies_data:
            # Check if title & format combo exists
            statement = select(Movie).where(Movie.title == m_data.title, Movie.format == m_data.format)
            existing_movie = session.exec(statement).first()

            if not existing_movie:
                try:
                    movie_service.create(m_data)
                    print(f"-----> Creating movie: {m_data.title}, Format: {m_data.format}")
                except HTTPException as e:
                    print(f"###### Error creating movie {m_data.title}: {e.detail}")
            else:
                print(f"-----> Movie '{m_data.title}' ({m_data.format}) already exists. Skipping.")
        
        session.commit()
    print("Seed of movies completed successfully!")

if __name__ == "__main__":
    seed_movie()