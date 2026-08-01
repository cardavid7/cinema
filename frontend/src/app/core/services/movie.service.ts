import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Movie } from '../../shared/models';

const API_BASE = '/api/v1/movies';

@Injectable({ providedIn: 'root' })
export class MovieService {
  constructor(private readonly http: HttpClient) {}

  getAll(): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${API_BASE}/`);
  }

  getById(movieId: number): Observable<Movie> {
    return this.http.get<Movie>(`${API_BASE}/${movieId}`);
  }

  searchByTitle(title: string): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${API_BASE}/title/${encodeURIComponent(title)}`);
  }
}
