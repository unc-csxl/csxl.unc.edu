import { Component, OnDestroy, OnInit } from '@angular/core';
import { Route } from '@angular/router';
import { Observable, Subscription, map, timer, tap } from 'rxjs';
import { Reservation } from 'src/app/coworking/coworking.models';
import { permissionGuard } from 'src/app/permission.guard';
import { AmbassadorRoomService } from './ambassador-room.service';

@Component({
  selector: 'app-ambassador-room-list',
  templateUrl: './ambassador-room-list.component.html',
  styleUrls: ['./ambassador-room-list.component.css']
})
export class AmbassadorRoomListComponent implements OnInit, OnDestroy {
  public static Route: Route = {
    path: 'room',
    component: AmbassadorRoomListComponent,
    title: 'Room Reservations',
    canActivate: [permissionGuard('coworking.reservation.*', '*')],
    resolve: {}
  };

  reservations$: Observable<Reservation[]>;
  upcomingReservations$: Observable<Reservation[]>;
  activeReservations$: Observable<Reservation[]>;

  columnsToDisplay = ['id', 'name', 'room', 'date', 'start', 'end', 'actions'];

  private refreshSubscription!: Subscription;

  constructor(public ambassadorService: AmbassadorRoomService) {
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
