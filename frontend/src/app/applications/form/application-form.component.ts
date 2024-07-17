import { Component } from '@angular/core';

@Component({
  selector: 'app-application-form',
  templateUrl: './application-form.component.html',
  styleUrl: './application-form.component.css'
})
export class ApplicationFormComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: ':type',
    title: 'Apply',
    component: ApplicationFormComponent,
    canActivate: []
  };
}
