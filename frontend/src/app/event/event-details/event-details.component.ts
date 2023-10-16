import { Component } from '@angular/core';
import { Organization } from 'src/app/organization/organization.service';
import { profileResolver } from 'src/app/profile/profile.resolver';

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
    resolve: { profile: profileResolver }
  }

  sampleOrganization: Organization

  constructor() {
    this.sampleOrganization = {
      id: 1,
      name: "HackNC",
      slug: "HackNC",
      logo: "https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/hacknc.jpg",
      short_description: "Organizes UNC's annual co-ed inclusive, beginner-friendly hackathon.",
      long_description: "HackNC is a weekend for students of all skill levels to broaden their talents. Your challenge is to make an awesome project in just 24 hours. You will have access to hands-on workshops and demos from our sponsors, as well as exciting talks about the awesome things happening right now with computer science and technology - not to mention all of the free food, shirts, stickers, and swag!",
      website: "https://hacknc.com/",
      email: "hacknsea@gmail.com",
      instagram: "",
      linked_in: "",
      youtube: "https://www.youtube.com/channel/UCDRN6TMC27uSDsZosIwUrZg",
      heel_life: "https://heellife.unc.edu/organization/hacknc",
      public: false,
      shorthand: ""
    }
  }
}
