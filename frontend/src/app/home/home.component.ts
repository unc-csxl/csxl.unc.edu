/**
 * The Home Component is the home page of the CSXL web application.
 * 
 * @author Kris Jordan
 * @copyright 2023
 * @license MIT
 */

import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html'
})
export class HomeComponent {
  public static Route = {
    path: '',
    component: HomeComponent
  }
}
