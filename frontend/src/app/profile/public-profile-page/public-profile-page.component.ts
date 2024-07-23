import { Component } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { publicProfileResolver } from '../profile.resolver';
import { PublicProfile } from '../profile.service';

@Component({
  selector: 'app-public-profile-page',
  templateUrl: './public-profile-page.component.html',
  styleUrl: './public-profile-page.component.css'
})
export class PublicProfilePageComponent {
  public static Route: Route = {
    path: ':onyen',
    component: PublicProfilePageComponent,
    title: 'Profile Page',
    canActivate: [isAuthenticated],
    resolve: {
      profile: publicProfileResolver
    }
  };

  profile: PublicProfile;

  constructor(private route: ActivatedRoute) {
    /** Get currently-logged-in user. */
    const data = this.route.snapshot.data as {
      profile: PublicProfile;
    };
    this.profile = data.profile;
  }
}
