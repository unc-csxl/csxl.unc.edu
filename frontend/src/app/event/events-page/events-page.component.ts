/**
 * The Event Page Component serves as a hub for students to browse all of the
 * events hosted by CS Organizations at UNC.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Component } from '@angular/core';

@Component({
  selector: 'app-events-page',
  templateUrl: './events-page.component.html',
  styleUrl: './events-page.component.css'
})
export class EventsPageComponent {
  /** Route information to be used in App Routing Module */
  public static Route = {
    path: '',
    title: 'Events',
    component: EventsPageComponent,
    canActivate: []
  };
}
