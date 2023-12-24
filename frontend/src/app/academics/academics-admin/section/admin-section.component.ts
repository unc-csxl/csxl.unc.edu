import { Component } from '@angular/core';
import { permissionGuard } from 'src/app/permission.guard';

@Component({
  selector: 'app-admin-section',
  templateUrl: './admin-section.component.html',
  styleUrls: ['./admin-section.component.css']
})
export class AdminSectionComponent {
  public static Route = {
    path: 'section',
    component: AdminSectionComponent,
    title: 'Section Administration',
    canActivate: [permissionGuard('academics.course', '*')]
  };
}
