import { Component, OnDestroy, OnInit } from '@angular/core';
import { Route } from '@angular/router';
import { Observable, Subscription, map, timer, tap } from 'rxjs';
import { Reservation } from 'src/app/coworking/coworking.models';
import { permissionGuard } from 'src/app/permission.guard';
import { AmbassadorXlService } from '../ambassador-xl.service';

@Component({
  selector: 'app-ambassador-xl-list',
  templateUrl: './ambassador-xl-list.component.html',
  styleUrls: ['./ambassador-xl-list.component.css']
})
export class AmbassadorXlListComponent implements OnDestroy, OnInit {
  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: 'xl',
    component: AmbassadorXlListComponent,
    title: 'XL Ambassador',
    canActivate: [permissionGuard('coworking.reservation.*', '*')],
    resolve: {}
  };

  reservations$: Observable<Reservation[]>;
  upcomingReservations$: Observable<Reservation[]>;
  activeReservations$: Observable<Reservation[]>;

  columnsToDisplay = ['id', 'name', 'seat', 'start', 'end', 'actions'];

  private refreshSubscription!: Subscription;

  constructor(public ambassadorService: AmbassadorXlService) {
    this.reservations$ = this.ambassadorService.reservations$;
    this.upcomingReservations$ = this.reservations$.pipe(
      map((reservations) => reservations.filter((r) => r.state === 'CONFIRMED'))
    );
    this.activeReservations$ = this.reservations$.pipe(
      map((reservations) =>
        reservations.filter((r) => r.state === 'CHECKED_IN')
      )
    );
  }

  ngOnInit(): void {
    this.refreshSubscription = timer(0, 5000)
      .pipe(tap((_) => this.ambassadorService.fetchReservations()))
      .subscribe();
  }

  ngOnDestroy(): void {
    this.refreshSubscription.unsubscribe();
  }
}
