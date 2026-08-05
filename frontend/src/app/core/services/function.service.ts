import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CinemaFunction, FunctionCreate, FunctionUpdate } from '../../shared/models';
import { environment } from '../../../environments/environment';

const API_BASE = `${environment.apiUrl}/api/v1/functions`;

@Injectable({ providedIn: 'root' })
export class FunctionService {
  constructor(private readonly http: HttpClient) {}

  getAll(): Observable<CinemaFunction[]> {
    return this.http.get<CinemaFunction[]>(`${API_BASE}/`);
  }

  getById(functionId: number): Observable<CinemaFunction> {
    return this.http.get<CinemaFunction>(`${API_BASE}/${functionId}`);
  }

  getAllByMovieId(movieId: number): Observable<CinemaFunction[]> {
    return this.http.get<CinemaFunction[]>(`${API_BASE}/movie/${movieId}`);
  }

  getAllByRoomId(roomId: number): Observable<CinemaFunction[]> {
    return this.http.get<CinemaFunction[]>(`${API_BASE}/room/${roomId}`);
  }

  create(fn: FunctionCreate): Observable<CinemaFunction> {
    return this.http.post<CinemaFunction>(`${API_BASE}/`, fn);
  }

  update(functionId: number, fn: FunctionUpdate): Observable<CinemaFunction> {
    return this.http.put<CinemaFunction>(`${API_BASE}/${functionId}`, fn);
  }

  delete(functionId: number): Observable<void> {
    return this.http.delete<void>(`${API_BASE}/${functionId}`);
  }
}
