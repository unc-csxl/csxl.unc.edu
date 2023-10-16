import { Component } from '@angular/core';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { eventDetailResolver } from '../event.resolver';
import { Profile } from 'src/app/profile/profile.service';
import { ActivatedRoute, ActivatedRouteSnapshot, ResolveFn } from '@angular/router';
import { Event } from '../event.service';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['event'].name;
};

@Component({
  selector: 'app-event-details',
  templateUrl: './event-details.component.html',
  styleUrls: ['./event-details.component.css']
})
export class EventDetailsComponent {

  /** Route information to be used in App Routing Module */
  public static Route = {
    path: ':id',
    title: 'Event Detail - TODO: Make Title Dynamic',
    component: EventDetailsComponent,
    resolve: { profile: profileResolver, event: eventDetailResolver },
    children: [{ path: '', title: titleResolver, component: EventDetailsComponent }]
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
