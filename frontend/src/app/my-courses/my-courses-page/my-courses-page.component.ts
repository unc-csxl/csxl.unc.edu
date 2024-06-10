import { Component } from '@angular/core';

@Component({
  selector: 'app-my-courses-page',
  templateUrl: './my-courses-page.component.html',
  styleUrl: './my-courses-page.component.css'
})
export class MyCoursesPageComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: '',
    title: 'My Courses',
    component: MyCoursesPageComponent
  };
}
