import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Reservation, ReservationCreate } from '../../shared/models';
import { environment } from '../../../environments/environment';

const API_BASE = `${environment.apiUrl}/api/v1/reservations`;

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

  cancel(reservationId: number): Observable<Reservation> {
    return this.http.put<Reservation>(`${API_BASE}/${reservationId}`, { status: 'CANCELLED' });
  }
}
