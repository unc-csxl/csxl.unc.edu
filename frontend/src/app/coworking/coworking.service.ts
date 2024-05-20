/**
 * @author Kris Jordan, John Schachte
 * @copyright 2023
 * @license MIT
 */

import { HttpClient } from '@angular/common/http';
import { Injectable, OnDestroy } from '@angular/core';
import { Observable, Subscription, map, BehaviorSubject } from 'rxjs';
import {
  CoworkingStatus,
  CoworkingStatusJSON,
  ReservationJSON,
  SeatAvailability,
  parseCoworkingStatusJSON,
  parseReservationJSON,
  Reservation
} from './coworking.models';
import { ProfileService } from '../profile/profile.service';
import { Profile } from '../models.module';
import { RxCoworkingStatus } from './rx-coworking-status';

const ONE_HOUR = 60 * 60 * 1000;

@Injectable({
  providedIn: 'root'
})
export class CoworkingService implements OnDestroy {
  private status: RxCoworkingStatus = new RxCoworkingStatus();
  public status$: Observable<CoworkingStatus> = this.status.value$;

  private profile: Profile | undefined;
  private profileSubscription!: Subscription;

  isCancelExpanded = new BehaviorSubject<boolean>(false);

  public findActiveReservationPredicate: (r: Reservation) => boolean = (
    r: Reservation
  ) => {
    let now = new Date();
    let soon = new Date(
      Date.now() + 10 /* minutes */ * 60 /* seconds */ * 1000 /* milliseconds */
    );
    const activeStates = ['DRAFT', 'CONFIRMED', 'CHECKED_IN'];
    return r.start <= soon && r.end > now && activeStates.includes(r.state);
  };

  public constructor(
    protected http: HttpClient,
    protected profileSvc: ProfileService
  ) {
    this.profileSubscription = this.profileSvc.profile$.subscribe(
      (profile) => (this.profile = profile)
    );
  }

  ngOnDestroy(): void {
    this.profileSubscription.unsubscribe();
  }

  pollStatus(): void {
    this.http
      .get<CoworkingStatusJSON>('/api/coworking/status')
      .pipe(map(parseCoworkingStatusJSON))
      .subscribe((status) => this.status.set(status));
  }

  draftReservation(seatSelection: SeatAvailability[]) {
    if (this.profile === undefined) {
      throw new Error('Only allowed for logged in users.');
    }

    let start = seatSelection[0].availability[0].start;
    let end = new Date(start.getTime() + 2 * ONE_HOUR);
    let reservation = {
      users: [this.profile],
      seats: seatSelection.map((seatAvailability) => {
        return { id: seatAvailability.id };
      }),
      start,
      end
    };

    return this.http
      .post<ReservationJSON>('/api/coworking/reservation', reservation)
      .pipe(map(parseReservationJSON));
  }

  /**
   * Toggles the expansion state of the cancellation UI.
   *
   * This method inverts the current boolean state of `isCancelExpanded`.
   * If `isCancelExpanded` is currently true, calling this method will set it to false, and vice versa.
   * This is typically used to control the visibility of a UI element that allows the user to cancel an action.
   *
   * @example
   * // Assuming `isCancelExpanded` is initially false
   * toggleCancelExpansion();
   * // Now `isCancelExpanded` is true
   *
   * @returns {void}
   */
  toggleCancelExpansion(): void {
    this.isCancelExpanded.next(!this.isCancelExpanded.value);
  }
}
