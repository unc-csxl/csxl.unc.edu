import { Component, OnInit } from '@angular/core';
import { MyCoursesService } from '../my-courses.service';

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

  constructor(public myCoursesService: MyCoursesService) {}
}
