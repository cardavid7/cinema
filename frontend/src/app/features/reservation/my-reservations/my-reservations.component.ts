import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';
import { AuthService } from '../../../core/services/auth.service';
import { ReservationService } from '../../../core/services/reservation.service';
import { Reservation } from '../../../shared/models';
import { extractErrorMessage } from '../../../shared/utils/http-error';

@Component({
  selector: 'app-my-reservations',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './my-reservations.component.html'
})
export class MyReservationsComponent {
  private readonly authService = inject(AuthService);
  private readonly reservationService = inject(ReservationService);

  readonly reservations = signal<Reservation[]>([]);
  readonly loading = signal(true);
  readonly errorMessage = signal<string | null>(null);
  readonly cancellingId = signal<number | null>(null);

  constructor() {
    this.load();
  }

  private load(): void {
    const userId = this.authService.currentUserId();
    if (!userId) {
      this.loading.set(false);
      return;
    }

    this.loading.set(true);
    this.reservationService
      .getByUserId(userId)
      .pipe(catchError(() => of([])))
      .subscribe((reservations) => {
        this.reservations.set(
          [...reservations].sort((a, b) => b.created_at.localeCompare(a.created_at))
        );
        this.loading.set(false);
      });
  }

  cancel(reservation: Reservation): void {
    this.cancellingId.set(reservation.id);
    this.errorMessage.set(null);

    this.reservationService.cancel(reservation.id).subscribe({
      next: () => {
        this.cancellingId.set(null);
        this.load();
      },
      error: (err) => {
        this.cancellingId.set(null);
        this.errorMessage.set(extractErrorMessage(err, 'No se pudo cancelar la reserva.'));
      }
    });
  }
}
