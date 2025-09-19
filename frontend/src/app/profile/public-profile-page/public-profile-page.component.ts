import { Component } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { publicProfileResolver } from '../profile.resolver';
import { PublicProfile } from '../profile.service';
import { SocialMediaIconWidgetService } from 'src/app/shared/social-media-icon/social-media-icon.widget.service';

@Component({
    selector: 'app-public-profile-page',
    templateUrl: './public-profile-page.component.html',
    styleUrl: './public-profile-page.component.css',
    standalone: false
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

  constructor(
    private route: ActivatedRoute,
    private icons: SocialMediaIconWidgetService
  ) {
    /** Get currently-logged-in user. */
    const data = this.route.snapshot.data as {
      profile: PublicProfile;
    };
    this.profile = data.profile;
  }
}
