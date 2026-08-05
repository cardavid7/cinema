export interface Room {
  id: number;
  name: string;
  capacity: number;
}

export interface RoomCreate {
  name: string;
  capacity: number;
}

export type RoomUpdate = Partial<RoomCreate>;
