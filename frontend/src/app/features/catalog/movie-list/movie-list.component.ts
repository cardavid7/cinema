import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { MovieService } from '../../../core/services/movie.service';
import { Movie } from '../../../shared/models';

@Component({
  selector: 'app-movie-list',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './movie-list.component.html'
})
export class MovieListComponent {
  private readonly movieService = inject(MovieService);
  private readonly fb = inject(FormBuilder);

  readonly movies = signal<Movie[]>([]);
  readonly loading = signal(true);
  readonly errorMessage = signal<string | null>(null);

  readonly searchForm = this.fb.nonNullable.group({ title: [''] });

  constructor() {
    this.loadAll();
  }

  loadAll(): void {
    this.loading.set(true);
    this.errorMessage.set(null);
    this.movieService.getAll().subscribe({
      next: (movies) => {
        this.movies.set(movies);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('No se pudo cargar el catálogo de películas.');
        this.loading.set(false);
      }
    });
  }

  search(): void {
    const title = this.searchForm.getRawValue().title.trim();
    if (!title) {
      this.loadAll();
      return;
    }

    this.loading.set(true);
    this.errorMessage.set(null);
    this.movieService.searchByTitle(title).subscribe({
      next: (movies) => {
        this.movies.set(movies);
        this.loading.set(false);
      },
      error: () => {
        this.movies.set([]);
        this.loading.set(false);
        this.errorMessage.set(`Sin resultados para "${title}".`);
      }
    });
  }
}
