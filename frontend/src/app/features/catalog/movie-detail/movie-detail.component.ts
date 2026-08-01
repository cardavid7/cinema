import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, forkJoin, of } from 'rxjs';
import { FunctionService } from '../../../core/services/function.service';
import { MovieService } from '../../../core/services/movie.service';
import { CinemaFunction, Movie } from '../../../shared/models';

@Component({
  selector: 'app-movie-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './movie-detail.component.html'
})
export class MovieDetailComponent {
  private readonly route = inject(ActivatedRoute);
  private readonly movieService = inject(MovieService);
  private readonly functionService = inject(FunctionService);

  readonly movie = signal<Movie | null>(null);
  readonly functions = signal<CinemaFunction[]>([]);
  readonly loading = signal(true);
  readonly errorMessage = signal<string | null>(null);

  constructor() {
    const movieId = Number(this.route.snapshot.paramMap.get('id'));

    forkJoin({
      movie: this.movieService.getById(movieId),
      functions: this.functionService.getAllByMovieId(movieId).pipe(catchError(() => of([])))
    }).subscribe({
      next: ({ movie, functions }) => {
        this.movie.set(movie);
        this.functions.set(functions);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('No se pudo cargar la película.');
        this.loading.set(false);
      }
    });
  }
}
