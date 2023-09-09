import { Component } from '@angular/core';
import { Route } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Observable, map } from 'rxjs';
import { Reservation } from '../coworking.models';
import { AmbassadorService } from './ambassador.service';

@Component({
  selector: 'app-coworking-ambassador-page',
  templateUrl: './ambassador-page.component.html',
  styleUrls: ['./ambassador-page.component.css']
})
export class AmbassadorPageComponent {

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

  columnsToDisplay = ['name', 'seat', 'start', 'end', 'actions'];

  constructor(public ambassadorService: AmbassadorService) {
    this.reservations$ = this.ambassadorService.reservations$;
    this.upcomingReservations$ = this.reservations$.pipe(map(reservations => reservations.filter(r => r.state === 'CONFIRMED')));
    this.ambassadorService.fetchReservations();
  }

  checkIn(reservation: Reservation) {
    this.ambassadorService.checkIn(reservation);
  }

}
