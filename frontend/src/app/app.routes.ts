import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./features/catalog/movie-list/movie-list.component').then((m) => m.MovieListComponent)
  },
  {
    path: 'movies/:id',
    loadComponent: () =>
      import('./features/catalog/movie-detail/movie-detail.component').then((m) => m.MovieDetailComponent)
  },
  {
    path: 'auth/login',
    loadComponent: () => import('./features/auth/login/login.component').then((m) => m.LoginComponent)
  },
  {
    path: 'auth/register',
    loadComponent: () =>
      import('./features/auth/register/register.component').then((m) => m.RegisterComponent)
  },
  {
    path: 'account',
    loadComponent: () => import('./features/home/home.component').then((m) => m.HomeComponent),
    canActivate: [authGuard]
  },
  { path: '**', redirectTo: '' }
];
