/**
 * The Coworking Component serves as the hub for students to create reservations
 * for tables, rooms, and equipment from the CSXL.
 * 
 * @author Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { CoworkingService } from '../coworking.service';
import { CoworkingStatus, OperatingHours, Reservation } from '../coworking.models';
import { Observable, map } from 'rxjs';

@Component({
  selector: 'app-coworking-page',
  templateUrl: './coworking-page.component.html',
  styleUrls: ['./coworking-page.component.css']
})
export class CoworkingPageComponent implements OnInit {

  public status$: Observable<CoworkingStatus>;

  public nextOperatingHours$: Observable<OperatingHours | undefined>;
  public isOpen$: Observable<boolean>;

  public activeReservation$: Observable<Reservation | undefined>;

  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: 'coworking',
    component: CoworkingPageComponent,
    title: 'Coworking',
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  constructor(route: ActivatedRoute, private router: Router, private coworkingService: CoworkingService) {
    this.status$ = coworkingService.status$;
    this.nextOperatingHours$ = this.initNextOperatingHours();
    this.isOpen$ = this.initIsOpen();
    this.activeReservation$ = this.initActiveReservation();
  }
  
  ngOnInit(): void {
    this.coworkingService.pullStatus();
  }

  private initNextOperatingHours(): Observable<OperatingHours | undefined> {
    return this.status$.pipe(map(status => {
      let now = new Date();
      return status.operating_hours.find(hours => hours.start <= now);
    }));
  }

  private initIsOpen(): Observable<boolean> {
    return this.nextOperatingHours$.pipe(map(hours => {
      let now = new Date();
      return hours !== undefined && hours.start <= now && hours.end > now;
    }));
  }

  private initActiveReservation(): Observable<Reservation | undefined> {
    return this.status$.pipe(map(status => {
      let reservations = status.my_reservations;
      let now = new Date();
      return reservations.find(reservation => reservation.start <= now && reservation.end > now);
    }));
  }

}
