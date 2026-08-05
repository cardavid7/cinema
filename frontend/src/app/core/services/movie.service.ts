import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Movie, MovieCreate, MovieUpdate } from '../../shared/models';
import { environment } from '../../../environments/environment';

const API_BASE = `${environment.apiUrl}/api/v1/movies`;

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

  create(movie: MovieCreate): Observable<Movie> {
    return this.http.post<Movie>(`${API_BASE}/`, movie);
  }

  update(movieId: number, movie: MovieUpdate): Observable<Movie> {
    return this.http.put<Movie>(`${API_BASE}/${movieId}`, movie);
  }

  delete(movieId: number): Observable<void> {
    return this.http.delete<void>(`${API_BASE}/${movieId}`);
  }
}
