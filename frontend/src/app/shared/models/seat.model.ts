export interface Seat {
  id: number;
  room_id: number;
  seat_number: string;
  is_vip: boolean;
}

export interface SeatCreate {
  room_id: number;
  seat_number: string;
  is_vip: boolean;
}

export type SeatUpdate = Partial<SeatCreate>;
