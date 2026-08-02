import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import { FunctionService } from '../../../core/services/function.service';
import { MovieService } from '../../../core/services/movie.service';
import { RoomService } from '../../../core/services/room.service';
import { CinemaFunction, Movie, Room } from '../../../shared/models';
import { extractErrorMessage } from '../../../shared/utils/http-error';

@Component({
  selector: 'app-admin-functions',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './admin-functions.component.html'
})
export class AdminFunctionsComponent {
  private readonly fb = inject(FormBuilder);
  private readonly functionService = inject(FunctionService);
  private readonly movieService = inject(MovieService);
  private readonly roomService = inject(RoomService);

  readonly functions = signal<CinemaFunction[]>([]);
  readonly movies = signal<Movie[]>([]);
  readonly rooms = signal<Room[]>([]);
  readonly loading = signal(true);
  readonly errorMessage = signal<string | null>(null);
  readonly editingId = signal<number | null>(null);

  readonly form = this.fb.nonNullable.group({
    movie_id: [0, [Validators.required, Validators.min(1)]],
    room_id: [0, [Validators.required, Validators.min(1)]],
    start_time: ['', Validators.required],
    price: [0, [Validators.required, Validators.min(0)]]
  });

  constructor() {
    this.load();
  }

  private load(): void {
    this.loading.set(true);
    forkJoin({
      functions: this.functionService.getAll(),
      movies: this.movieService.getAll(),
      rooms: this.roomService.getAll()
    }).subscribe({
      next: ({ functions, movies, rooms }) => {
        this.functions.set(functions);
        this.movies.set(movies);
        this.rooms.set(rooms);
        this.loading.set(false);
        if (!this.editingId()) {
          this.form.patchValue({ movie_id: movies[0]?.id ?? 0, room_id: rooms[0]?.id ?? 0 });
        }
      },
      error: () => {
        this.errorMessage.set('No se pudo cargar el listado.');
        this.loading.set(false);
      }
    });
  }

  startCreate(): void {
    this.editingId.set(null);
    this.form.reset({
      movie_id: this.movies()[0]?.id ?? 0,
      room_id: this.rooms()[0]?.id ?? 0,
      start_time: '',
      price: 0
    });
  }

  startEdit(fn: CinemaFunction): void {
    this.editingId.set(fn.id);
    this.form.setValue({
      movie_id: fn.movie_id,
      room_id: fn.room_id,
      start_time: fn.start_time.slice(0, 16),
      price: fn.price
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
    const request = id ? this.functionService.update(id, value) : this.functionService.create(value);

    request.subscribe({
      next: () => {
        this.startCreate();
        this.load();
      },
      error: (err) => this.errorMessage.set(extractErrorMessage(err, 'No se pudo guardar la función.'))
    });
  }

  remove(fn: CinemaFunction): void {
    if (!confirm(`¿Eliminar esta función?`)) {
      return;
    }
    this.functionService.delete(fn.id).subscribe({
      next: () => this.load(),
      error: (err) => this.errorMessage.set(extractErrorMessage(err, 'No se pudo eliminar la función.'))
    });
  }
}
