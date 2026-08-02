import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Seat } from '../../shared/models';

const API_BASE = '/api/v1/seats';

@Injectable({ providedIn: 'root' })
export class SeatService {
  constructor(private readonly http: HttpClient) {}

  getByRoomId(roomId: number): Observable<Seat[]> {
    const params = new HttpParams().set('room_id', roomId);
    return this.http.get<Seat[]>(`${API_BASE}/`, { params });
  }
}
