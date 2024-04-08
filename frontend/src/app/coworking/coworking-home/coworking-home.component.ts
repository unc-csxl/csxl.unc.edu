/**
 * The Coworking Component serves as the hub for students to create reservations
 * for tables, rooms, and equipment from the CSXL.
 *
 * @author Kris Jordan, Ajay Gandecha, John Schachte
 * @copyright 2023
 * @license MIT
 */

import { Component, OnDestroy, OnInit } from '@angular/core';
import { Route, Router } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { CoworkingService } from '../coworking.service';
import { ProfileService } from 'src/app/profile/profile.service';
import {
  CoworkingStatus,
  OperatingHours,
  Reservation,
  SeatAvailability
} from '../coworking.models';
import { Observable, Subscription, map, mergeMap, of, timer, catchError } from 'rxjs';
import { RoomReservationService } from '../room-reservation/room-reservation.service';
import { ReservationService } from '../reservation/reservation.service';
import { MatDialog } from '@angular/material/dialog';
import { CommunityAgreement } from 'src/app/shared/community-agreement/community-agreement.widget';
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

  public upcomingReservations$: Observable<Reservation[] | undefined>;

  private timerSubscription!: Subscription;

  public upcomingRoomReservation$!: Observable<Reservation[]>;

  public filteredRoomReservations$!: Observable<Reservation[]>;

  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: '',
    component: CoworkingPageComponent,
    title: 'Coworking',
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  constructor(
    public coworkingService: CoworkingService,
    private router: Router,
    private reservationService: ReservationService,
    protected snackBar: MatSnackBar,
    private roomReservationService: RoomReservationService,
    private profileService: ProfileService,
    private dialog: MatDialog
  ) {
    this.status$ = coworkingService.status$;
    this.openOperatingHours$ = this.initNextOperatingHours();
    this.isOpen$ = this.initIsOpen();
    this.activeReservation$ = this.initActiveReservation();
    this.upcomingReservations$ = this.initUpcomingReservations();

  }

  /**
   * A lifecycle hook that is called after Angular has initialized all data-bound properties of a directive.
   *
   * Use this hook to initialize the directive or component. This is the right place to fetch data from a server,
   * set up any local state, or perform operations that need to be executed only once when the component is instantiated.
   *
   * @returns {void} - This method does not return a value.
   */
  ngOnInit(): void {
    this.status$ = this.coworkingService.status$;
    this.openOperatingHours$ = this.initNextOperatingHours();
    this.isOpen$ = this.initIsOpen();
    this.activeReservation$ = this.initActiveReservation();
    this.timerSubscription = timer(0, 10000).subscribe(() => {
      this.coworkingService.pollStatus();
    });
  }

  reserve(seatSelection: SeatAvailability[]) {
    this.coworkingService.draftReservation(seatSelection).subscribe({
      error: (error) =>
        this.snackBar.open(
          'Error. There may be a conflicting upcoming reservation. Please check upcoming reservations.',
          '',
          { duration: 8000 }
        ),
      next: (reservation) => {
        this.router.navigateByUrl(`/coworking/reservation/${reservation.id}`);
      }
    });
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
        return reservations.find(
          this.coworkingService.findActiveReservationPredicate
        );
      }),
      mergeMap((reservation) =>
        reservation
          ? this.reservationService.get(reservation.id)
          : of(undefined)
      )
    );
  }

  initUpcomingReservations(): Observable<Reservation[]> {
    const isUpcomingRoomReservation = (r: Reservation) =>
      !this.coworkingService.findActiveReservationPredicate(r) && !!r && !!r.room
      && r.state == 'CONFIRMED';
  
    return this.status$
      .pipe(
        map((status) => {
          let reservations = status.my_reservations;
          return reservations.filter((r) => isUpcomingRoomReservation(r));
        }),
        catchError((err: Error) => {
          const message = 'Error while fetching upcoming reservations.';
          this.snackBar.open(message, '', { duration: 8000 });
          console.error(err);
          return of([]);
        })
      );
  }
  
  navigateToNewReservation() {
    this.router.navigateByUrl('/coworking/new-reservation');
  }

  /**
   * Function that is used when coworking card triggers a need to refresh the active reservation
   */
  setActiveReservation() {
    this.activeReservation$ = this.initActiveReservation();
  }

  private hasAcceptedAgreement() {
    this.profileService.profile$.subscribe((profile) => {
      if (profile) {
        if (profile.accepted_community_agreement === false) {
          const dialogRef = this.dialog.open(CommunityAgreement, {
            width: '1000px',
            disableClose: true,
            autoFocus: false
          });
          dialogRef.afterClosed().subscribe();
        }
      }
    });
  }
}
