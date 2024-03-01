import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ReservationTableService } from '../reservation-table.service';
import { Reservation } from 'src/app/coworking/coworking.models';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { catchError, Observable, of } from 'rxjs';
import { RoomReservationService } from '../room-reservation.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-new-reservation-page',
  templateUrl: './new-reservation-page.component.html',
  styleUrls: ['./new-reservation-page.component.css']
})
export class NewReservationPageComponent implements OnInit {
  public static Route = {
    path: 'new-reservation',
    title: 'New Reservation',
    component: NewReservationPageComponent,
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  public upcomingRoomReservations$!: Observable<Reservation[]>;
  public numHoursStudyRoomReservations$!: Observable<string>;

  constructor(
    private router: Router,
    private reservationTableService: ReservationTableService,
    private roomReservationService: RoomReservationService,
    protected snackBar: MatSnackBar
  ) {}

  ngOnInit() {
    this.handleUpdateReservationsList();
    this.getNumHoursStudyRoomReservations();
  }

  navigateToNewReservation() {
    this.router.navigateByUrl('/coworking/new-reservation');
  }

  handleUpdateReservationsList() {
    this.upcomingRoomReservations$ = this.roomReservationService
      .getReservationsByState('CONFIRMED')
      .pipe(
        catchError((err) => {
          const message = 'Error while fetching upcoming reservations.';
          this.snackBar.open(message, '', { duration: 8000 });
          console.error(err);
          return of([]);
        })
      );
  }
  getNumHoursStudyRoomReservations() {
    this.numHoursStudyRoomReservations$ =
      this.roomReservationService.getNumHoursStudyRoomReservations();
  }
}
