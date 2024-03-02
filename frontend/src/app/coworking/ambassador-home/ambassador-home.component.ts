import { Component, OnDestroy, OnInit } from '@angular/core';
import { Route } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import {
  Observable,
  ReplaySubject,
  Subscription,
  debounceTime,
  filter,
  map,
  mergeMap,
  startWith,
  tap,
  timer
} from 'rxjs';
import {
  CoworkingStatus,
  Reservation,
  SeatAvailability
} from '../coworking.models';
import { AmbassadorService } from './ambassador.service';
import { FormControl } from '@angular/forms';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { Profile } from 'src/app/models.module';
import { ProfileService, PublicProfile } from 'src/app/profile/profile.service';
import { CoworkingService } from '../coworking.service';

@Component({
  selector: 'app-coworking-ambassador-home',
  templateUrl: './ambassador-home.component.html',
  styleUrls: ['./ambassador-home.component.css']
})
export class AmbassadorPageComponent implements OnInit, OnDestroy {
  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: 'ambassador',
    component: AmbassadorPageComponent,
    title: 'XL Ambassador',
    canActivate: [permissionGuard('coworking.reservation.*', '*')],
    resolve: { profile: profileResolver }
  };

  reservations$: Observable<Reservation[]>;
  upcomingReservations$: Observable<Reservation[]>;
  activeReservations$: Observable<Reservation[]>;

  welcomeDeskReservationSelection: PublicProfile[] = [];
  status$: Observable<CoworkingStatus>;

  columnsToDisplay = ['id', 'name', 'seat', 'start', 'end', 'actions'];

  private refreshSubscription!: Subscription;

  constructor(
    public ambassadorService: AmbassadorService,
    public profileService: ProfileService,
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

  ngOnInit(): void {
    this.refreshSubscription = timer(0, 50000)
      .pipe(tap((_) => this.ambassadorService.fetchReservations()))
      .subscribe();
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
            // Hack to force the pull of new reservations
            this.ngOnDestroy();
            this.ngOnInit();
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
