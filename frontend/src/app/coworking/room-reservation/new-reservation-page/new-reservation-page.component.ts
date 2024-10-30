/**
 * @author John Schachte, Aarjav Jain, Nick Wherthey
 * @copyright 2023
 * @license MIT
 */

import { Component, input, OnInit, signal, Signal, WritableSignal } from '@angular/core';
import { Router } from '@angular/router';
import { Reservation } from 'src/app/coworking/coworking.models';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { catchError, Observable, of } from 'rxjs';
import { RoomReservationService } from '../room-reservation.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatFormFieldControl } from '@angular/material/form-field';
import { FormControl, Validators } from '@angular/forms';

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

  public numHoursStudyRoomReservations$!: Observable<string>;
  // public capacity = new FormControl<number | null>(0, Validators.required);
  public capacity = new FormControl<number | null>(null, [Validators.required, Validators.min(1)])

  constructor(
    private router: Router,
    private roomReservationService: RoomReservationService,
    protected snackBar: MatSnackBar
  ) {}

  /**
   * A lifecycle hook that is called after Angular has initialized all data-bound properties of a directive.
   *
   * Use this hook to initialize the directive or component. This is the right place to fetch data from a server,
   * set up any local state, or perform operations that need to be executed only once when the component is instantiated.
   *
   * @returns {void} - This method does not return a value.
   */

  ngOnInit() {
    this.getNumHoursStudyRoomReservations();
  }

  navigateToNewReservation() {
    this.router.navigateByUrl('/coworking/new-reservation');
  }

  getNumHoursStudyRoomReservations() {
    this.numHoursStudyRoomReservations$ =
      this.roomReservationService.getNumHoursStudyRoomReservations();
  }

  updateCapacity() {
    if (this.capacity.value === null) {
      console.log("null");
    } else {
      console.log("Current capacity:", this.capacity.value);
    }
  }
}
