/**
 * @author John Schachte, Aarjav Jain, Nick Wherthey
 * @copyright 2023
 * @license MIT
 */

import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Router } from '@angular/router';
import { timer } from 'rxjs';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Reservation } from '../../coworking.models';
import { RoomReservationService } from '../room-reservation.service';

@Component({
  selector: 'app-confirm-reservation',
  templateUrl: './confirm-reservation.component.html',
  styleUrls: ['./confirm-reservation.component.css']
})
export class ConfirmReservationComponent implements OnInit, OnDestroy {
  public static Route = {
    path: 'confirm-reservation/:id',
    title: 'Confirm Reservation',
    component: ConfirmReservationComponent,
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  reservation: Reservation | null = null; // Declaration of the reservation property
  isConfirmed: boolean = false; // flag to see if reservation was confirmed

  public id: number;

  constructor(
    private roomReservationService: RoomReservationService,
    protected snackBar: MatSnackBar,
    private router: Router,
    public route: ActivatedRoute
  ) {
    this.id = parseInt(this.route.snapshot.params['id']);
  }

  ngOnDestroy(): void {
    if (this.isConfirmed) return;
    this.roomReservationService
      .deleteRoomReservation(this.reservation!)
      .subscribe();
  }

  /**
   * A lifecycle hook that is called after Angular has initialized all data-bound properties of a directive.
   *
   * Use this hook to initialize the directive or component. This is the right place to fetch data from a server,
   * set up any local state, or perform operations that need to be executed only once when the component is instantiated.
   *
   * @returns {void} - This method does not return a value.
   */
  ngOnInit() {
    this.roomReservationService.get(this.id).subscribe({
      next: (response) => (this.reservation = response), // Assume only one draft per user
      error: (error) => {
        this.snackBar.open('Error while fetching draft reservation.', '', {
          duration: 8000
        });
        timer(3000).subscribe(() =>
          this.router.navigateByUrl('/coworking/new-reservation')
        );
        console.error(error.message);
      }
    });
  }

  setConfirmation(isConfirmed: boolean) {
    this.isConfirmed = isConfirmed;
  }
}
