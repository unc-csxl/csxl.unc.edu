import { Component } from '@angular/core';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { eventDetailResolver } from '../event.resolver';
import { Profile } from 'src/app/profile/profile.service';
import { ActivatedRoute } from '@angular/router';
import { Event } from '../event.service';

@Component({
  selector: 'app-event-details',
  templateUrl: './event-details.component.html',
  styleUrls: ['./event-details.component.css']
})
export class EventDetailsComponent {

  /** Route information to be used in App Routing Module */
  public static Route = {
    path: 'detail',
    title: 'Event Detail - TODO: Make Title Dynamic',
    component: EventDetailsComponent,
    canActivate: [],
    resolve: { profile: profileResolver, event: eventDetailResolver }
  }

  /** Store Event */
  public event!: Event;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

    
  constructor(private route: ActivatedRoute) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as { profile: Profile, event: Event };
    this.profile = data.profile;
    this.event = data.event;
  }
}
