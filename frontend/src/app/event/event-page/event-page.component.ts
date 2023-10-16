import { Component, HostListener } from '@angular/core';
import { Organization } from 'src/app/organization/organization.service';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { eventResolver } from '../event.resolver';
import { ActivatedRoute } from '@angular/router';
import { Profile } from 'src/app/profile/profile.service';
import { Event } from '../event.service';

@Component({
  selector: 'app-event-page',
  templateUrl: './event-page.component.html',
  styleUrls: ['./event-page.component.css']
})
export class EventPageComponent {

  /** Route information to be used in App Routing Module */
  public static Route = {
    path: '',
    title: 'Events',
    component: EventPageComponent,
    canActivate: [],
    resolve: { profile: profileResolver, events: eventResolver }
  }

  /** Store Observable list of Events */
  public events: Event[];

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Stores the width of the window. */
  public innerWidth: any;

  constructor(private route: ActivatedRoute) {

    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as { profile: Profile, events: Event[] };
    this.profile = data.profile;
    this.events = data.events;
    console.log(data.events);
  }

  ngOnInit() {
      this.innerWidth = window.innerWidth;
  }

  @HostListener('window:resize', ['$event'])
  onResize(_: UIEvent) {
    this.innerWidth = window.innerWidth;
  }
}

export interface EventDetailData {
  name: string;
  organization: Organization;
  startText: string;
  endText: string;
  location: string;
  description: string;
  requiresPreregistration: boolean;
}
