import { Component } from '@angular/core';
import { profileResolver } from '../profile/profile.resolver';
import { EventsService, Event } from './events.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-events',
  templateUrl: './events.component.html',
  styleUrls: ['./events.component.css']
})
export class EventsComponent {

  public events$: Observable<Event[]>;

  public static Route = { 
    path: 'events',
    title: 'Events',
    component: EventsComponent,
    canActivate: [],
    resolve: { profile: profileResolver } 
  }

  constructor(private eventsService: EventsService) {
    this.events$ = this.eventsService.getEvents();
    }

}