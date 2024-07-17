import { Component } from '@angular/core';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrl: './admin.component.css'
})
export class AdminComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'admin',
    title: 'Admin',
    component: AdminComponent
  };

  constructor() {}
}
