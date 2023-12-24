import { Component } from '@angular/core';
import { permissionGuard } from 'src/app/permission.guard';

@Component({
  selector: 'app-admin-term',
  templateUrl: './admin-term.component.html',
  styleUrls: ['./admin-term.component.css']
})
export class AdminTermComponent {
  public static Route = {
    path: 'term',
    component: AdminTermComponent,
    title: 'Term Administration',
    canActivate: [permissionGuard('academics.course', '*')]
  };
}
