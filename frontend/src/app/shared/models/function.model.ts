import { Movie } from './movie.model';
import { Room } from './room.model';

export interface CinemaFunction {
  id: number;
  movie_id: number;
  room_id: number;
  start_time: string;
  end_time: string;
  price: number;
  movie?: Movie;
  room?: Room;
}

export interface FunctionCreate {
  movie_id: number;
  room_id: number;
  start_time: string;
  price: number;
}

export type FunctionUpdate = FunctionCreate;
