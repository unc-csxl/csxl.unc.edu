import { Component } from '@angular/core';

@Component({
  selector: 'app-student-section-home',
  templateUrl: './student-section-home.component.html',
  styleUrls: ['./student-section-home.component.css']
})
export class StudentSectionHomeComponent {
  public static Route = {
    path: 'course/semester',
    title: 'Office Hours',
    component: StudentSectionHomeComponent,
    canActivate: []
  };
}
