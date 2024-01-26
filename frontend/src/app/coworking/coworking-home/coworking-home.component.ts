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
import { ProfileService } from 'src/app/profile/profile.service';
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
import { MatDialog } from '@angular/material/dialog';
import { CommunityAgreement } from 'src/app/shared/community-agreement/community-agreement.widget';

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
    private profileService: ProfileService,
    private dialog: MatDialog
  ) {
    this.status$ = coworkingService.status$;
    this.openOperatingHours$ = this.initNextOperatingHours();
    this.isOpen$ = this.initIsOpen();
    this.activeReservation$ = this.initActiveReservation();
  }

  reserve(seatSelection: SeatAvailability[]) {
    this.coworkingService.draftReservation(seatSelection).subscribe({
      next: (reservation) => {
        this.router.navigateByUrl(`/coworking/reservation/${reservation.id}`);
      }
    });
  }

  ngOnInit(): void {
    this.timerSubscription = timer(0, 10000).subscribe(() =>
      this.coworkingService.pollStatus()
    );
    this.hasAgreed();
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

  private hasAgreed() {
    this.profileService.profile$.subscribe((profile) => {
      if (profile) {
        console.log('profile when accessing home page:', profile);
        if (profile.has_agreed === false) {
          const dialogRef = this.dialog.open(CommunityAgreement, {
            width: '1000px'
            // height: '1000px'
          });
          dialogRef.afterClosed().subscribe((result) => {
            console.log('Dialog closed with result:', result);
            // Send updated profile to backend after user agrees
          });
        }
      }
    });
  }
}
