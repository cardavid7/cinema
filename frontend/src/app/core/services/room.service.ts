import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Room, RoomCreate, RoomUpdate } from '../../shared/models';

const API_BASE = '/api/v1/rooms';

@Injectable({ providedIn: 'root' })
export class RoomService {
  constructor(private readonly http: HttpClient) {}

  getAll(): Observable<Room[]> {
    return this.http.get<Room[]>(`${API_BASE}/`);
  }

  getById(roomId: number): Observable<Room> {
    return this.http.get<Room>(`${API_BASE}/${roomId}`);
  }

  create(room: RoomCreate): Observable<Room> {
    return this.http.post<Room>(`${API_BASE}/`, room);
  }

  update(roomId: number, room: RoomUpdate): Observable<Room> {
    return this.http.put<Room>(`${API_BASE}/${roomId}`, room);
  }

  delete(roomId: number): Observable<void> {
    return this.http.delete<void>(`${API_BASE}/${roomId}`);
  }
}
