import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { RoomService } from '../../../core/services/room.service';
import { SeatService } from '../../../core/services/seat.service';
import { Room, Seat } from '../../../shared/models';
import { extractErrorMessage } from '../../../shared/utils/http-error';

@Component({
  selector: 'app-admin-seats',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './admin-seats.component.html'
})
export class AdminSeatsComponent {
  private readonly fb = inject(FormBuilder);
  private readonly seatService = inject(SeatService);
  private readonly roomService = inject(RoomService);

  readonly rooms = signal<Room[]>([]);
  readonly seats = signal<Seat[]>([]);
  readonly selectedRoomId = signal<number | null>(null);
  readonly loading = signal(true);
  readonly errorMessage = signal<string | null>(null);
  readonly editingId = signal<number | null>(null);

  readonly form = this.fb.nonNullable.group({
    seat_number: ['', Validators.required],
    is_vip: [false]
  });

  constructor() {
    this.roomService.getAll().subscribe({
      next: (rooms) => {
        this.rooms.set(rooms);
        this.loading.set(false);
        if (rooms.length > 0) {
          this.selectRoom(rooms[0].id);
        }
      },
      error: () => {
        this.errorMessage.set('No se pudieron cargar las salas.');
        this.loading.set(false);
      }
    });
  }

  selectRoom(roomId: number): void {
    this.selectedRoomId.set(roomId);
    this.startCreate();
    this.loadSeats();
  }

  private loadSeats(): void {
    const roomId = this.selectedRoomId();
    if (!roomId) {
      return;
    }
    this.seatService.getByRoomId(roomId).subscribe({
      next: (seats) => this.seats.set(seats),
      error: () => this.errorMessage.set('No se pudieron cargar los asientos.')
    });
  }

  startCreate(): void {
    this.editingId.set(null);
    this.form.reset({ seat_number: '', is_vip: false });
  }

  startEdit(seat: Seat): void {
    this.editingId.set(seat.id);
    this.form.setValue({ seat_number: seat.seat_number, is_vip: seat.is_vip });
  }

  submit(): void {
    const roomId = this.selectedRoomId();
    if (this.form.invalid || !roomId) {
      this.form.markAllAsTouched();
      return;
    }

    this.errorMessage.set(null);
    const value = { ...this.form.getRawValue(), room_id: roomId };
    const id = this.editingId();
    const request = id ? this.seatService.update(id, value) : this.seatService.create(value);

    request.subscribe({
      next: () => {
        this.startCreate();
        this.loadSeats();
      },
      error: (err) => this.errorMessage.set(extractErrorMessage(err, 'No se pudo guardar el asiento.'))
    });
  }

  remove(seat: Seat): void {
    if (!confirm(`¿Eliminar el asiento ${seat.seat_number}?`)) {
      return;
    }
    this.seatService.delete(seat.id).subscribe({
      next: () => this.loadSeats(),
      error: (err) => this.errorMessage.set(extractErrorMessage(err, 'No se pudo eliminar el asiento.'))
    });
  }
}
