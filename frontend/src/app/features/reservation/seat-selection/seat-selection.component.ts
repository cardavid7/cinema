import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, forkJoin, of } from 'rxjs';
import { FunctionService } from '../../../core/services/function.service';
import { ReservationService } from '../../../core/services/reservation.service';
import { SeatService } from '../../../core/services/seat.service';
import { CinemaFunction, Seat } from '../../../shared/models';
import { extractErrorMessage } from '../../../shared/utils/http-error';

interface SeatRow {
  label: string;
  seats: Seat[];
}

@Component({
  selector: 'app-seat-selection',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './seat-selection.component.html'
})
export class SeatSelectionComponent {
  private readonly route = inject(ActivatedRoute);
  private readonly functionService = inject(FunctionService);
  private readonly seatService = inject(SeatService);
  private readonly reservationService = inject(ReservationService);

  private readonly functionId = Number(this.route.snapshot.paramMap.get('id'));

  readonly cinemaFunction = signal<CinemaFunction | null>(null);
  readonly seats = signal<Seat[]>([]);
  readonly occupiedSeatIds = signal<Set<number>>(new Set());
  readonly selectedSeat = signal<Seat | null>(null);

  readonly loading = signal(true);
  readonly errorMessage = signal<string | null>(null);
  readonly submitting = signal(false);
  readonly confirmedReservationId = signal<number | null>(null);

  readonly seatRows = computed<SeatRow[]>(() => {
    const rows = new Map<string, Seat[]>();
    for (const seat of this.seats()) {
      const label = seat.seat_number.match(/^[A-Za-z]+/)?.[0] ?? seat.seat_number;
      if (!rows.has(label)) {
        rows.set(label, []);
      }
      rows.get(label)!.push(seat);
    }
    return Array.from(rows.entries())
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([label, seatList]) => ({
        label,
        seats: seatList.sort((a, b) => a.seat_number.localeCompare(b.seat_number, undefined, { numeric: true }))
      }));
  });

  constructor() {
    this.loadData();
  }

  private loadData(): void {
    this.loading.set(true);
    this.errorMessage.set(null);

    this.functionService.getById(this.functionId).subscribe({
      next: (fn) => {
        this.cinemaFunction.set(fn);
        this.loadSeatsAndReservations(fn.room_id);
      },
      error: () => {
        this.errorMessage.set('No se pudo cargar la función.');
        this.loading.set(false);
      }
    });
  }

  private loadSeatsAndReservations(roomId: number): void {
    forkJoin({
      seats: this.seatService.getByRoomId(roomId),
      reservations: this.reservationService.getByFunctionId(this.functionId).pipe(catchError(() => of([])))
    }).subscribe({
      next: ({ seats, reservations }) => {
        this.seats.set(seats);
        this.occupiedSeatIds.set(
          new Set(reservations.filter((r) => r.status === 'CONFIRMED').map((r) => r.seat_id))
        );
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('No se pudieron cargar los asientos.');
        this.loading.set(false);
      }
    });
  }

  isOccupied(seat: Seat): boolean {
    return this.occupiedSeatIds().has(seat.id);
  }

  selectSeat(seat: Seat): void {
    if (this.isOccupied(seat)) {
      return;
    }
    this.selectedSeat.set(seat);
  }

  confirmReservation(): void {
    const seat = this.selectedSeat();
    if (!seat) {
      return;
    }

    this.submitting.set(true);
    this.errorMessage.set(null);

    this.reservationService
      .create({ function_id: this.functionId, seat_id: seat.id, status: 'CONFIRMED' })
      .subscribe({
        next: (reservation) => {
          this.submitting.set(false);
          this.confirmedReservationId.set(reservation.id);
        },
        error: (err) => {
          this.submitting.set(false);
          if (err.status === 400) {
            this.errorMessage.set('Ese asiento ya fue reservado por otra persona. Elegí otro.');
            this.selectedSeat.set(null);
            this.loadSeatsAndReservations(this.cinemaFunction()!.room_id);
          } else {
            this.errorMessage.set(extractErrorMessage(err, 'No se pudo completar la reserva.'));
          }
        }
      });
  }
}
