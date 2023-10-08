/**
 * The Reservation Page Component shows the details of an individual reservation and handles its operations.
 * 
 * @author Kris Jordan
 * @copyright 2023
 * @license MIT
 */

import { Component } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';

@Component({
  selector: 'app-coworking-reservation',
  templateUrl: './reservation.component.html',
  styleUrls: ['./reservation.component.css']
})
export class ReservationComponent {

  public static Route: Route = {
    path: 'reservation/:id',
    component: ReservationComponent,
    title: 'Reservation',
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  public id: string = "";

  constructor(public route: ActivatedRoute) {
    this.id = route.snapshot.params['id'];
  }

}
