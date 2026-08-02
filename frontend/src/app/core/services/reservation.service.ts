import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Reservation, ReservationCreate } from '../../shared/models';

const API_BASE = '/api/v1/reservations';

@Injectable({ providedIn: 'root' })
export class ReservationService {
  constructor(private readonly http: HttpClient) {}

  create(reservation: ReservationCreate): Observable<Reservation> {
    return this.http.post<Reservation>(`${API_BASE}/`, reservation);
  }

  getByFunctionId(functionId: number): Observable<Reservation[]> {
    return this.http.get<Reservation[]>(`${API_BASE}/function/${functionId}`);
  }

  getByUserId(userId: number): Observable<Reservation[]> {
    return this.http.get<Reservation[]>(`${API_BASE}/user/${userId}`);
  }

  cancel(reservationId: number): Observable<void> {
    return this.http.delete<void>(`${API_BASE}/${reservationId}`);
  }
}
