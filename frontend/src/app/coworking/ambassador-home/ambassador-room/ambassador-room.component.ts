import { Component, OnDestroy, OnInit, computed } from '@angular/core';
import { Route } from '@angular/router';
import { Subscription, timer, tap } from 'rxjs';
import { permissionGuard } from 'src/app/permission.guard';
import { AmbassadorRoomService } from './ambassador-room.service';

@Component({
  selector: 'app-ambassador-room',
  templateUrl: './ambassador-room.component.html',
  styleUrls: ['./ambassador-room.component.css']
})
export class AmbassadorRoomComponent implements OnInit, OnDestroy {
  public static Route: Route = {
    path: 'room',
    component: AmbassadorRoomComponent,
    title: 'Room Reservations',
    canActivate: [permissionGuard('coworking.reservation.*', '*')],
    resolve: {}
  };

  upcomingReservations = computed(() => {
    return this.ambassadorService.reservations().filter((r) => {
      return r.state == 'CONFIRMED';
    });
  });

  activeReservations = computed(() => {
    return this.ambassadorService.reservations().filter((r) => {
      return r.state == 'CHECKED_IN';
    });
  });

  columnsToDisplay = ['id', 'name', 'room', 'date', 'start', 'end', 'actions'];

  private refreshSubscription!: Subscription;

  constructor(public ambassadorService: AmbassadorRoomService) {}

  ngOnInit(): void {
    this.refreshSubscription = timer(0, 5000)
      .pipe(tap((_) => this.ambassadorService.fetchReservations()))
      .subscribe();
  }

  ngOnDestroy(): void {
    this.refreshSubscription.unsubscribe();
  }
}
