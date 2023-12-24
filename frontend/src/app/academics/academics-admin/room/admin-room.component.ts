import { Component } from '@angular/core';
import { permissionGuard } from 'src/app/permission.guard';

@Component({
  selector: 'app-admin-room',
  templateUrl: './admin-room.component.html',
  styleUrls: ['./admin-room.component.css']
})
export class AdminRoomComponent {
  public static Route = {
    path: 'room',
    component: AdminRoomComponent,
    title: 'Room Administration',
    canActivate: [permissionGuard('academics.term', '*')]
  };
}
