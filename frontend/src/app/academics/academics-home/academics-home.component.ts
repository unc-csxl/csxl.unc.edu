import { Component } from '@angular/core';

@Component({
  selector: 'app-academics-home',
  templateUrl: './academics-home.component.html',
  styleUrls: ['./academics-home.component.css']
})
export class AcademicsHomeComponent {
  /** Route information to be used in Course Routing Module */
  public static Route = {
    path: '',
    title: 'Academics',
    component: AcademicsHomeComponent,
    canActivate: []
  };
}
