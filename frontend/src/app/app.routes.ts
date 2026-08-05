import { Routes } from '@angular/router';
import { adminGuard } from './core/guards/admin.guard';
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
    path: 'functions/:id/seats',
    loadComponent: () =>
      import('./features/reservation/seat-selection/seat-selection.component').then(
        (m) => m.SeatSelectionComponent
      ),
    canActivate: [authGuard]
  },
  {
    path: 'account',
    loadComponent: () => import('./features/home/home.component').then((m) => m.HomeComponent),
    canActivate: [authGuard]
  },
  {
    path: 'account/reservations',
    loadComponent: () =>
      import('./features/reservation/my-reservations/my-reservations.component').then(
        (m) => m.MyReservationsComponent
      ),
    canActivate: [authGuard]
  },
  {
    path: 'admin',
    loadComponent: () =>
      import('./features/admin/admin-dashboard/admin-dashboard.component').then(
        (m) => m.AdminDashboardComponent
      ),
    canActivate: [adminGuard]
  },
  {
    path: 'admin/movies',
    loadComponent: () =>
      import('./features/admin/admin-movies/admin-movies.component').then((m) => m.AdminMoviesComponent),
    canActivate: [adminGuard]
  },
  {
    path: 'admin/rooms',
    loadComponent: () =>
      import('./features/admin/admin-rooms/admin-rooms.component').then((m) => m.AdminRoomsComponent),
    canActivate: [adminGuard]
  },
  {
    path: 'admin/functions',
    loadComponent: () =>
      import('./features/admin/admin-functions/admin-functions.component').then(
        (m) => m.AdminFunctionsComponent
      ),
    canActivate: [adminGuard]
  },
  {
    path: 'admin/seats',
    loadComponent: () =>
      import('./features/admin/admin-seats/admin-seats.component').then((m) => m.AdminSeatsComponent),
    canActivate: [adminGuard]
  },
  { path: '**', redirectTo: '' }
];
