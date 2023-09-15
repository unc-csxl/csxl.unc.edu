/**
 * The Coworking Component serves as the hub for students to create reservations
 * for tables, rooms, and equipment from the CSXL.
 * 
 * @author Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { CoworkingService } from '../coworking.service';
import { CoworkingStatus, OperatingHours, Reservation, SeatAvailability } from '../coworking.models';
import { Observable, Subscription, map, timer } from 'rxjs';

@Component({
  selector: 'app-coworking-page',
  templateUrl: './coworking-page.component.html',
  styleUrls: ['./coworking-page.component.css']
})
export class CoworkingPageComponent implements OnInit, OnDestroy {

  public status$: Observable<CoworkingStatus>;

  public openOperatingHours$: Observable<OperatingHours | undefined>;
  public isOpen$: Observable<boolean>;

  public activeReservation$: Observable<Reservation | undefined>;

  private timerSubscription!: Subscription;

  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: '',
    component: CoworkingPageComponent,
    title: 'Coworking',
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  constructor(route: ActivatedRoute, private router: Router, public coworkingService: CoworkingService) {
    this.status$ = coworkingService.status$;
    this.openOperatingHours$ = this.initNextOperatingHours();
    this.isOpen$ = this.initIsOpen();
    this.activeReservation$ = this.initActiveReservation();
  }

  reserve(seatSelection: SeatAvailability[]) {
    this.coworkingService.draftReservation(seatSelection).subscribe();
  }

  cancel(reservation: Reservation) {
    this.coworkingService.cancelReservation(reservation);
  }

  ngOnInit(): void {
    this.timerSubscription = timer(0, 10000).subscribe(() => this.coworkingService.pollStatus());
  }

  ngOnDestroy(): void {
    this.timerSubscription.unsubscribe();
  }

  private initNextOperatingHours(): Observable<OperatingHours | undefined> {
    return this.status$.pipe(map(status => {
      let now = new Date();
      return status.operating_hours.find(hours => hours.start <= now);
    }));
  }

  private initIsOpen(): Observable<boolean> {
    return this.openOperatingHours$.pipe(map(hours => {
      let now = new Date();
      return hours !== undefined && hours.start <= now && hours.end > now;
    }));
  }

  private initActiveReservation(): Observable<Reservation | undefined> {
    return this.status$.pipe(map(status => {
      let reservations = status.my_reservations;
      let now = new Date();
      return reservations.find(reservation => reservation.end > now);
    }));
  }

}
