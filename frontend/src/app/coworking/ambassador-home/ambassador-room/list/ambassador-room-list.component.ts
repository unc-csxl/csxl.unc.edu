import { Component } from '@angular/core';
import { Route } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';

@Component({
  selector: 'app-ambassador-room-list',
  templateUrl: './ambassador-room-list.component.html',
  styleUrls: ['./ambassador-room-list.component.css']
})
export class AmbassadorRoomListComponent {
  public static Route: Route = {
    path: 'room',
    component: AmbassadorRoomListComponent,
    title: 'Room Reservations',
    canActivate: [permissionGuard('coworking.reservation.*', '*')],
    resolve: {}
  };
}
