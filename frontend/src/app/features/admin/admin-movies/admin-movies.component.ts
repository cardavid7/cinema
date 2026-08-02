import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { MovieService } from '../../../core/services/movie.service';
import { Movie, MovieFormat } from '../../../shared/models';
import { extractErrorMessage } from '../../../shared/utils/http-error';

@Component({
  selector: 'app-admin-movies',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './admin-movies.component.html'
})
export class AdminMoviesComponent {
  private readonly fb = inject(FormBuilder);
  private readonly movieService = inject(MovieService);

  readonly movies = signal<Movie[]>([]);
  readonly loading = signal(true);
  readonly errorMessage = signal<string | null>(null);
  readonly editingId = signal<number | null>(null);
  readonly formats: MovieFormat[] = ['2D', '2D_SUB', '3D', '3D_SUB'];

  readonly form = this.fb.nonNullable.group({
    title: ['', Validators.required],
    description: ['', Validators.required],
    duration: [90, [Validators.required, Validators.min(1)]],
    format: ['2D' as MovieFormat, Validators.required]
  });

  constructor() {
    this.load();
  }

  private load(): void {
    this.loading.set(true);
    this.movieService.getAll().subscribe({
      next: (movies) => {
        this.movies.set(movies);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('No se pudo cargar el listado.');
        this.loading.set(false);
      }
    });
  }

  startCreate(): void {
    this.editingId.set(null);
    this.form.reset({ title: '', description: '', duration: 90, format: '2D' });
  }

  startEdit(movie: Movie): void {
    this.editingId.set(movie.id);
    this.form.setValue({
      title: movie.title,
      description: movie.description,
      duration: movie.duration,
      format: movie.format
    });
  }

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.errorMessage.set(null);
    const value = this.form.getRawValue();
    const id = this.editingId();
    const request = id ? this.movieService.update(id, value) : this.movieService.create(value);

    request.subscribe({
      next: () => {
        this.startCreate();
        this.load();
      },
      error: (err) => this.errorMessage.set(extractErrorMessage(err, 'No se pudo guardar la película.'))
    });
  }

  remove(movie: Movie): void {
    if (!confirm(`¿Eliminar "${movie.title}"?`)) {
      return;
    }
    this.movieService.delete(movie.id).subscribe({
      next: () => this.load(),
      error: (err) => this.errorMessage.set(extractErrorMessage(err, 'No se pudo eliminar la película.'))
    });
  }
}
