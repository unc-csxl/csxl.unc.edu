import { Component } from '@angular/core';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrl: './settings.component.css'
})
export class SettingsComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'settings',
    title: 'Course',
    component: SettingsComponent
  };
}
