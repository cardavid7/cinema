from app.seeds.user import seed_user
from app.seeds.movie import seed_movie
from app.seeds.room import seed_rooms
from app.seeds.seat import seed_seat
from app.seeds.function import seed_function
from app.seeds.reservation import seed_reservation

def run_all_seeds():
    seed_user()
    seed_movie()
    seed_rooms()
    seed_seat()
    seed_function()
    seed_reservation()

if __name__ == "__main__":
    run_all_seeds()
