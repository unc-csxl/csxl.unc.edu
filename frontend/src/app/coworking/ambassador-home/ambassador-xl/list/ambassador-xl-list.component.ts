import { Component, OnDestroy, OnInit } from '@angular/core';
import { Route } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Observable, Subscription, map, tap, timer } from 'rxjs';
import {
  CoworkingStatus,
  Reservation,
  SeatAvailability
} from '../../../coworking.models';
import { AmbassadorXlService } from '../ambassador-xl.service';
import { PublicProfile } from 'src/app/profile/profile.service';
import { CoworkingService } from '../../../coworking.service';

const FIVE_SECONDS = 5 * 1000;

@Component({
  selector: 'app-ambassador-xl-list',
  templateUrl: './ambassador-xl-list.component.html',
  styleUrls: ['./ambassador-xl-list.component.css']
})
export class AmbassadorXlListComponent implements OnDestroy, OnInit {
  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: 'xl',
    component: AmbassadorXlListComponent,
    title: 'XL Reservations',
    canActivate: [permissionGuard('coworking.reservation.*', '*')],
    resolve: {}
  };

  reservations$: Observable<Reservation[]>;
  upcomingReservations$: Observable<Reservation[]>;
  activeReservations$: Observable<Reservation[]>;

  welcomeDeskReservationSelection: PublicProfile[] = [];
  status$: Observable<CoworkingStatus>;

  columnsToDisplay = ['id', 'name', 'seat', 'start', 'end', 'actions'];

  private refreshSubscription!: Subscription;

  constructor(
    public ambassadorService: AmbassadorXlService,
    public coworkingService: CoworkingService
  ) {
    this.reservations$ = this.ambassadorService.reservations$;
    this.upcomingReservations$ = this.reservations$.pipe(
      map((reservations) => reservations.filter((r) => r.state === 'CONFIRMED'))
    );
    this.activeReservations$ = this.reservations$.pipe(
      map((reservations) =>
        reservations.filter((r) => r.state === 'CHECKED_IN')
      )
    );

    this.status$ = coworkingService.status$;
  }

  beginReservationRefresh(): void {
    if (this.refreshSubscription) {
      this.refreshSubscription.unsubscribe();
    }
    this.refreshSubscription = timer(0, FIVE_SECONDS)
      .pipe(tap((_) => this.ambassadorService.fetchReservations()))
      .subscribe();
  }

  ngOnInit(): void {
    this.beginReservationRefresh();
  }

  ngOnDestroy(): void {
    this.refreshSubscription.unsubscribe();
  }

  onUsersChanged(users: PublicProfile[]) {
    if (users.length > 0) {
      this.coworkingService.pollStatus();
    }
  }

  onWalkinSeatSelection(seatSelection: SeatAvailability[]) {
    if (
      seatSelection.length > 0 &&
      this.welcomeDeskReservationSelection.length > 0
    ) {
      this.ambassadorService
        .makeDropinReservation(
          seatSelection,
          this.welcomeDeskReservationSelection
        )
        .subscribe({
          next: (reservation) => {
            this.welcomeDeskReservationSelection = [];
            this.beginReservationRefresh();
            alert(
              `Walk-in reservation made for ${
                reservation.users[0].first_name
              } ${
                reservation.users[0].last_name
              }!\nReservation ends at ${reservation.end.toLocaleTimeString()}`
            );
          },
          error: (e) => {
            this.welcomeDeskReservationSelection = [];
            alert(e.message + '\n\n' + e.error.message);
          }
        });
    }
  }
}
