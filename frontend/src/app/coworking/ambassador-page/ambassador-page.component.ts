import { Component } from '@angular/core';
import { Route } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { CoworkingService } from '../coworking.service';
import { Observable } from 'rxjs';
import { Reservation } from '../coworking.models';

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

  constructor(public coworkingSvc: CoworkingService) {
    this.reservations$ = coworkingSvc.listActiveAndUpcomingReservations();
  }

}
