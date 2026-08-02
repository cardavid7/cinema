import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, computed, signal } from '@angular/core';
import { Observable, tap } from 'rxjs';
import { AuthCredentials, AuthResponse, User } from '../../shared/models';

const TOKEN_KEY = 'cinema_access_token';
const API_BASE = '/api/v1';

function decodeUserId(token: string | null): number | null {
  if (!token) {
    return null;
  }
  try {
    const payload = token.split('.')[1];
    const normalized = payload.replace(/-/g, '+').replace(/_/g, '/');
    const { sub } = JSON.parse(atob(normalized));
    return sub ? Number(sub) : null;
  } catch {
    return null;
  }
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly tokenSignal = signal<string | null>(localStorage.getItem(TOKEN_KEY));

  readonly token = computed(() => this.tokenSignal());
  readonly isAuthenticated = computed(() => !!this.tokenSignal());
  readonly currentUserId = computed(() => decodeUserId(this.tokenSignal()));

  constructor(private readonly http: HttpClient) {}

  register(credentials: AuthCredentials): Observable<User> {
    return this.http.post<User>(`${API_BASE}/auth/register`, credentials);
  }

  login(credentials: AuthCredentials): Observable<AuthResponse> {
    const params = new HttpParams()
      .set('email', credentials.email)
      .set('password', credentials.password);

    return this.http
      .post<AuthResponse>(`${API_BASE}/auth/login`, null, { params })
      .pipe(tap((response) => this.setToken(response.access_token)));
  }

  logout(): void {
    this.setToken(null);
  }

  private setToken(token: string | null): void {
    if (token) {
      localStorage.setItem(TOKEN_KEY, token);
    } else {
      localStorage.removeItem(TOKEN_KEY);
    }
    this.tokenSignal.set(token);
  }
}
