/**
 * The Coworking Component serves as the hub for students to create reservations
 * for tables, rooms, and equipment from the CSXL.
 *
 * @author Kris Jordan, Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { CoworkingService } from '../coworking.service';
import {
  CoworkingStatus,
  OperatingHours,
  Reservation,
  SeatAvailability
} from '../coworking.models';
import {
  Observable,
  Subscription,
  filter,
  map,
  mergeMap,
  of,
  timer
} from 'rxjs';
import { ReservationService } from '../reservation/reservation.service';
import { MatSnackBar } from '@angular/material/snack-bar';
@Component({
  selector: 'app-coworking-home',
  templateUrl: './coworking-home.component.html',
  styleUrls: ['./coworking-home.component.css']
})
export class CoworkingPageComponent implements OnInit, OnDestroy {
  public status$: Observable<CoworkingStatus>;

  public openOperatingHours$: Observable<OperatingHours | undefined>;
  public isOpen$: Observable<boolean>;

  public activeReservation$: Observable<Reservation | undefined>;

  private timerSubscription!: Subscription;

  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: '',
    component: CoworkingPageComponent,
    title: 'Coworking',
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  constructor(
    route: ActivatedRoute,
    public coworkingService: CoworkingService,
    private router: Router,
    private reservationService: ReservationService,
    protected snackBar: MatSnackBar
  ) {
    this.status$ = coworkingService.status$;
    this.openOperatingHours$ = this.initNextOperatingHours();
    this.isOpen$ = this.initIsOpen();
    this.activeReservation$ = this.initActiveReservation();
  }

  reserve(seatSelection: SeatAvailability[]) {
    this.coworkingService.draftReservation(seatSelection).subscribe({
      error: (error) =>
        this.snackBar.open(
          'Error. There may be a reservation in the next 2 hours. Please cancel that if you want to drop-in.',
          '',
          { duration: 8000 }
        ),
      next: (reservation) => {
        this.router.navigateByUrl(`/coworking/reservation/${reservation.id}`);
      }
    });
  }

  ngOnInit(): void {
    this.status$ = this.coworkingService.status$;
    this.openOperatingHours$ = this.initNextOperatingHours();
    this.isOpen$ = this.initIsOpen();
    this.activeReservation$ = this.initActiveReservation();
    this.timerSubscription = timer(0, 10000).subscribe(() =>
      this.coworkingService.pollStatus()
    );
  }

  ngOnDestroy(): void {
    this.timerSubscription.unsubscribe();
  }

  private initNextOperatingHours(): Observable<OperatingHours | undefined> {
    return this.status$.pipe(
      map((status) => {
        let now = new Date();
        return status.operating_hours.find((hours) => hours.start <= now);
      })
    );
  }

  private initIsOpen(): Observable<boolean> {
    return this.openOperatingHours$.pipe(
      map((hours) => {
        let now = new Date();
        return hours !== undefined && hours.start <= now && hours.end > now;
      })
    );
  }

  private initActiveReservation(): Observable<Reservation | undefined> {
    return this.status$.pipe(
      map((status) => {
        let reservations = status.my_reservations;
        let now = new Date();
        return reservations.find(
          (reservation) => reservation.start <= now && reservation.end > now
        );
      }),
      mergeMap((reservation) =>
        reservation
          ? this.reservationService.get(reservation.id)
          : of(undefined)
      )
    );
  }

  navigateToNewReservation() {
    this.router.navigateByUrl('/coworking/new-reservation');
  }

  /**
   * Function that is when coworking card triggers a need to refresh the active reservation
   */
  setActiveReservation() {
    this.activeReservation$ = this.initActiveReservation();
  }
}
