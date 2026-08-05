import { User } from './user.model';
import { CinemaFunction } from './function.model';
import { Seat } from './seat.model';

export type ReservationStatus = 'CONFIRMED' | 'CANCELLED';

export interface Reservation {
  id: number;
  user_id: number;
  function_id: number;
  seat_id: number;
  status: ReservationStatus;
  created_at: string;
  updated_at: string;
  user?: User;
  function?: CinemaFunction;
  seat?: Seat;
}

export interface ReservationCreate {
  function_id: number;
  seat_id: number;
  status: ReservationStatus;
}

export interface ReservationUpdate {
  status: ReservationStatus;
}
