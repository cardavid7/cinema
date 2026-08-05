import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { RoomService } from '../../../core/services/room.service';
import { Room } from '../../../shared/models';
import { extractErrorMessage } from '../../../shared/utils/http-error';

@Component({
  selector: 'app-admin-rooms',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './admin-rooms.component.html'
})
export class AdminRoomsComponent {
  private readonly fb = inject(FormBuilder);
  private readonly roomService = inject(RoomService);

  readonly rooms = signal<Room[]>([]);
  readonly loading = signal(true);
  readonly errorMessage = signal<string | null>(null);
  readonly editingId = signal<number | null>(null);

  readonly form = this.fb.nonNullable.group({
    name: ['', Validators.required],
    capacity: [20, [Validators.required, Validators.min(1)]]
  });

  constructor() {
    this.load();
  }

  private load(): void {
    this.loading.set(true);
    this.roomService.getAll().subscribe({
      next: (rooms) => {
        this.rooms.set(rooms);
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
    this.form.reset({ name: '', capacity: 20 });
  }

  startEdit(room: Room): void {
    this.editingId.set(room.id);
    this.form.setValue({ name: room.name, capacity: room.capacity });
  }

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.errorMessage.set(null);
    const value = this.form.getRawValue();
    const id = this.editingId();
    const request = id ? this.roomService.update(id, value) : this.roomService.create(value);

    request.subscribe({
      next: () => {
        this.startCreate();
        this.load();
      },
      error: (err) => this.errorMessage.set(extractErrorMessage(err, 'No se pudo guardar la sala.'))
    });
  }

  remove(room: Room): void {
    if (!confirm(`¿Eliminar "${room.name}"?`)) {
      return;
    }
    this.roomService.delete(room.id).subscribe({
      next: () => this.load(),
      error: (err) => this.errorMessage.set(extractErrorMessage(err, 'No se pudo eliminar la sala.'))
    });
  }
}
