import { Component } from '@angular/core';

@Component({
  selector: 'app-hiring-assignments',
  standalone: true,
  imports: [],
  templateUrl: './hiring-assignments.component.html',
  styleUrl: './hiring-assignments.component.css'
})
export class HiringAssignmentsComponent {
  /** Route for the routing module */
  public static Route = {
    path: ':courseSiteId/assignments',
    title: 'Hiring',
    component: HiringAssignmentsComponent
  };
}
