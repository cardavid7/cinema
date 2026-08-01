import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CinemaFunction } from '../../shared/models';

const API_BASE = '/api/v1/functions';

@Injectable({ providedIn: 'root' })
export class FunctionService {
  constructor(private readonly http: HttpClient) {}

  getById(functionId: number): Observable<CinemaFunction> {
    return this.http.get<CinemaFunction>(`${API_BASE}/${functionId}`);
  }

  getAllByMovieId(movieId: number): Observable<CinemaFunction[]> {
    return this.http.get<CinemaFunction[]>(`${API_BASE}/movie/${movieId}`);
  }

  getAllByRoomId(roomId: number): Observable<CinemaFunction[]> {
    return this.http.get<CinemaFunction[]>(`${API_BASE}/room/${roomId}`);
  }
}
