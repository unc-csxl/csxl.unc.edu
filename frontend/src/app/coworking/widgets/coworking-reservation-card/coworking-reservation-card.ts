import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Reservation } from 'src/app/coworking/coworking.models';
import { Observable, map, mergeMap, timer } from 'rxjs';
import { Router } from '@angular/router';
import { RoomReservationService } from '../../room-reservation/room-reservation.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'coworking-reservation-card',
  templateUrl: './coworking-reservation-card.html',
  styleUrls: ['./coworking-reservation-card.css']
})
export class CoworkingReservationCard implements OnInit {
  @Input() reservation!: Reservation;
  @Output() updateReservationsList = new EventEmitter<void>();
  @Output() isConfirmed = new EventEmitter<boolean>();
  @Output() updateActiveReservation = new EventEmitter<void>();
  @Output() reloadCoworkingHome = new EventEmitter<void>();

  public draftConfirmationDeadline$!: Observable<string>;

  constructor(
    public router: Router,
    public reservationService: RoomReservationService,
    protected snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.draftConfirmationDeadline$ = this.initDraftConfirmationDeadline();
  }

  checkinDeadline(reservationStart: Date): Date {
    return new Date(reservationStart.getTime() + 10 * 60 * 1000);
  }

  cancel() {
    this.reservationService.deleteRoomReservation(this.reservation).subscribe(
      () => {
        this.triggerUpdateReservationsList();
        this.router.navigateByUrl('/coworking');
      },
      (error: Error) => {
        this.snackBar.open(
          'Error: Issue cancelling reservation. Please see CSXL Ambassador for assistance.',
          '',
          { duration: 8000 }
        );
        console.error(error.message);
      }
    );
  }

  confirm() {
    this.isConfirmed.emit(true);
    this.reservationService.confirm(this.reservation).subscribe(
      () => this.router.navigateByUrl('/coworking'),
      (error: Error) => {
        this.snackBar.open(
          'Error: Issue confirming reservation. Please see CSXL Ambassador for assistance.',
          '',
          { duration: 8000 }
        );
        console.error(error.message);
      }
    );
  }

  checkout() {
    this.reservationService.checkout(this.reservation).subscribe({
      next: () => this.triggerUpdateReservationsList(),
      error: (error: Error) => {
        this.snackBar.open(
          'Error: Issue checking out reservation. Please see CSXL Ambassador for assistance.',
          '',
          { duration: 8000 }
        );
        console.error(error.message);
      }
    });
  }

  checkin(): void {
    this.reservationService.checkin(this.reservation).subscribe({
      next: () => {
        this.triggerUpdateReservationsList();
      },
      error: (error: Error) => {
        this.snackBar.open(
          'Error: Issue cancelling reservation. Please see CSXL Ambassador for assistance.',
          '',
          { duration: 8000 }
        );
      }
    });
  }

  private initDraftConfirmationDeadline(): Observable<string> {
    const fiveMinutes =
      5 /* minutes */ * 60 /* seconds */ * 1000; /* milliseconds */

    const reservationDraftDeadline = (reservation: Reservation) => {
      return new Date(reservation.created_at).getTime() + fiveMinutes;
    };

    const deadlineString = (deadline: number): string => {
      const now = new Date().getTime();
      const delta = (deadline - now) / 1000; /* milliseconds */
      if (delta > 60) {
        return `Confirm in ${Math.ceil(delta / 60)} minutes`;
      } else if (delta > 0) {
        return `Confirm in ${Math.ceil(delta)} seconds`;
      } else {
        this.cancel();
        return 'Cancelling...';
      }
    };

    return timer(0, 1000).pipe(
      map(() => this.reservation),
      map(reservationDraftDeadline),
      map(deadlineString)
    );
  }

  triggerUpdateReservationsList() {
    this.updateActiveReservation.emit();
    this.updateReservationsList.emit();
  }

  refreshCoworkingHome(): void {
    this.reloadCoworkingHome.emit();
  }

  checkCheckinAllowed(): boolean {
    let now = new Date();
    return (
      new Date(this.reservation!.start) <= now &&
      now <= new Date(this.reservation!.end)
    );
  }
}
