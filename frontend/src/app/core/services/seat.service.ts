import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Seat, SeatCreate, SeatUpdate } from '../../shared/models';
import { environment } from '../../../environments/environment';

const API_BASE = `${environment.apiUrl}/api/v1/seats`;

@Injectable({ providedIn: 'root' })
export class SeatService {
  constructor(private readonly http: HttpClient) {}

  getByRoomId(roomId: number): Observable<Seat[]> {
    const params = new HttpParams().set('room_id', roomId);
    return this.http.get<Seat[]>(`${API_BASE}/`, { params });
  }

  create(seat: SeatCreate): Observable<Seat> {
    return this.http.post<Seat>(`${API_BASE}/`, seat);
  }

  update(seatId: number, seat: SeatUpdate): Observable<Seat> {
    return this.http.put<Seat>(`${API_BASE}/${seatId}`, seat);
  }

  delete(seatId: number): Observable<void> {
    return this.http.delete<void>(`${API_BASE}/${seatId}`);
  }
}
