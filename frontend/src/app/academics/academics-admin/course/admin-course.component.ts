import { Component, inject } from '@angular/core';
import { permissionGuard } from 'src/app/permission.guard';

@Component({
  selector: 'app-admin-course',
  templateUrl: './admin-course.component.html',
  styleUrls: ['./admin-course.component.css']
})
export class AdminCourseComponent {
  public static Route = {
    path: 'course',
    component: AdminCourseComponent,
    title: 'Course Administration',
    canActivate: [permissionGuard('academics.course', '*')]
  };
}
