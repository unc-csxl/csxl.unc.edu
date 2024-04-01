/**
 * The Office Hours Page Component serves as the home page for the Office Hours feature.
 * 
 *
 * @author Madelyn Andrews, Bailey DeSouza, Meghan Sun, Sadie Amato
 * @copyright 2024
 * @license MIT
 */

import { Component } from '@angular/core';

@Component({
  selector: 'app-office-hours-page',
  templateUrl: './office-hours-page.component.html',
  styleUrls: ['./office-hours-page.component.css']
})
export class OfficeHoursPageComponent {
  public static Route = {
    path: '',
    title: 'Office Hours',
    component: OfficeHoursPageComponent,
    canActivate: []
  };
}
