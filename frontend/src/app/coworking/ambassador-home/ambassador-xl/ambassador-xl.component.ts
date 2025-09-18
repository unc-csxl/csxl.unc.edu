/**
 * @author Kris Jordan <kris@cs.unc.edu>, Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023 - 2024
 * @license MIT
 */

import { Component, OnDestroy, OnInit, Signal, computed } from '@angular/core';
import { Route } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { Subscription, timer } from 'rxjs';
import { CoworkingStatus, SeatAvailability } from '../../coworking.models';
import { AmbassadorXlService } from './ambassador-xl.service';
import { PublicProfile } from 'src/app/profile/profile.service';
import { CoworkingService } from '../../coworking.service';

const FIVE_SECONDS = 5 * 1000;

@Component({
    selector: 'app-ambassador-xl',
    templateUrl: './ambassador-xl.component.html',
    styleUrls: ['./ambassador-xl.component.css'],
    standalone: false
})
export class AmbassadorXLComponent implements OnDestroy, OnInit {
  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: 'xl',
    component: AmbassadorXLComponent,
    title: 'XL Reservations',
    canActivate: [permissionGuard('coworking.reservation.*', '*')],
    resolve: {}
  };

  upcomingReservations = computed(() => {
    return this.ambassadorService.reservations().filter((r) => {
      return r.state == 'CONFIRMED';
    });
  });

  activeReservations = computed(() => {
    return this.ambassadorService.reservations().filter((r) => {
      return r.state == 'CHECKED_IN';
    });
  });

  welcomeDeskReservationSelection: PublicProfile[] = [];
  status: Signal<CoworkingStatus>;

  columnsToDisplay = ['id', 'name', 'seat', 'start', 'end', 'actions'];

  private refreshSubscription!: Subscription;

  constructor(
    public ambassadorService: AmbassadorXlService,
    public coworkingService: CoworkingService
  ) {
    this.status = coworkingService.status;
  }

  beginReservationRefresh(): void {
    if (this.refreshSubscription) {
      this.refreshSubscription.unsubscribe();
    }
    this.refreshSubscription = timer(0, FIVE_SECONDS).subscribe((_) => {
      this.ambassadorService.fetchReservations();
    });
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
