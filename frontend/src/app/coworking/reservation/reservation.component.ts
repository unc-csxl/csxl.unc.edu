/**
 * The Reservation Page Component shows the details of an individual reservation and handles its operations.
 * 
 * @author Kris Jordan
 * @copyright 2023
 * @license MIT
 */

import { Component, inject } from '@angular/core';
import { ActivatedRoute, ActivatedRouteSnapshot, ResolveFn, Route, Router } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Observable, map, mergeMap, take, timer } from 'rxjs';
import { Reservation } from '../coworking.models';
import { ReservationService } from './reservation.service';

const titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot): Observable<string> => {
  let reservationService = inject(ReservationService);
  let reservationTitle = (reservation: Reservation): string => {
    return `Reservation #${reservation.id}`; // TODO: Include State of Reservation in future version
    // of this application when the fix for this bug lands: https://github.com/angular/angular/issues/51401
  };
  return reservationService.get(parseInt(route.params['id'])).pipe(map(reservationTitle));
};

@Component({
  selector: 'app-coworking-reservation',
  templateUrl: './reservation.component.html',
  styleUrls: ['./reservation.component.css'],
})
export class ReservationComponent {

  public static Route: Route = {
    path: 'reservation/:id',
    component: ReservationComponent,
    runGuardsAndResolvers: "always",
    title: titleResolver,
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  public id: number;
  public reservation$: Observable<Reservation>;
  public draftConfirmationDeadline$!: Observable<string>;

  constructor(public route: ActivatedRoute, public reservationService: ReservationService, public router: Router) {
    this.id = parseInt(route.snapshot.params['id']);
    this.reservation$ = reservationService.get(this.id);
    this.draftConfirmationDeadline$ = this.initDraftConfirmationDeadline();
  }

  checkinDeadline(reservationStart: Date): Date {
    return new Date(reservationStart.getTime() + (10 * 60 * 1000));
  }

  cancel(reservation: Reservation): void {
    this.reservationService.cancel(reservation).subscribe();
  }

  confirm(reservation: Reservation): void {
    this.reservationService.confirm(reservation).subscribe();
  }

  checkout(reservation: Reservation): void {
    this.reservationService.checkout(reservation).subscribe();
  }

  private initDraftConfirmationDeadline(): Observable<string> {

    const fiveMinutes = 5 /* minutes */ * 60 /* seconds */ * 1000 /* milliseconds */;

    const reservationDraftDeadline = (reservation: Reservation) => reservation.created_at.getTime() + fiveMinutes;

    const deadlineString = (deadline: number): string => {
      const now = (new Date().getTime())
      const delta = (deadline - now) / 1000 /* milliseconds */;
      if (delta > 60) {
        return `Confirm in ${Math.ceil(delta / 60)} minutes`;
      } else if (delta > 0) {
        return `Confirm in ${Math.ceil(delta)} seconds`;
      } else {
        this.reservation$.pipe(take(1)).subscribe(reservation => this.cancel(reservation));
        return "Cancelling...";
      }
    }

    return timer(0, 1000).pipe(
      mergeMap(() => this.reservation$),
      map(reservationDraftDeadline),
      map(deadlineString)
    );
  }

}
