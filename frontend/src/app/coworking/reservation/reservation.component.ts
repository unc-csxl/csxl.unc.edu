/**
 * The Reservation Page Component shows the details of an individual reservation and handles its operations.
 *
 * @author Kris Jordan
 * @copyright 2023
 * @license MIT
 */

import { Component, inject } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Route,
  Router
} from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Observable, map } from 'rxjs';
import { Reservation } from '../coworking.models';
import { ReservationService } from './reservation.service';

const titleResolver: ResolveFn<string> = (
  route: ActivatedRouteSnapshot
): Observable<string> => {
  let reservationService = inject(ReservationService);
  let reservationTitle = (reservation: Reservation): string => {
    return `Reservation #${reservation.id}`; // TODO: Include State of Reservation in future version
    // of this application when the fix for this bug lands: https://github.com/angular/angular/issues/51401
  };
  return reservationService
    .get(parseInt(route.params['id']))
    .pipe(map(reservationTitle));
};

@Component({
  selector: 'app-coworking-reservation',
  templateUrl: './reservation.component.html',
  styleUrls: ['./reservation.component.css']
})
export class ReservationComponent {
  public static Route: Route = {
    path: 'reservation/:id',
    component: ReservationComponent,
    title: titleResolver,
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  public id: number;
  public reservation$: Observable<Reservation>;

  constructor(
    public route: ActivatedRoute,
    public reservationService: ReservationService,
    public router: Router
  ) {
    this.id = parseInt(route.snapshot.params['id']);
    this.reservation$ = reservationService.get(this.id);
  }
}
