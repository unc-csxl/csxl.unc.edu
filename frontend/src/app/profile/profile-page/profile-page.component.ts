import { Component } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from '../profile.resolver';
import { Profile, ProfileService } from '../profile.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { EventService } from 'src/app/event/event.service';
import { Event } from '../../event/event.model';

@Component({
  selector: 'app-profile-page',
  templateUrl: './profile-page.component.html',
  styleUrls: ['./profile-page.component.css']
})
export class ProfilePageComponent {
  public static Route: Route = {
    path: '',
    component: ProfilePageComponent,
    title: 'Profile Page',
    canActivate: [isAuthenticated],
    resolve: {
      profile: profileResolver
    }
  };

  profile: Profile;

  public token: string;
  public showToken: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected eventService: EventService,
    protected profileService: ProfileService,
    protected snackBar: MatSnackBar
  ) {
    /** Get currently-logged-in user. */
    const data = this.route.snapshot.data as {
      profile: Profile;
      userEvents: Event[];
    };
    this.profile = data.profile;

    /** Switch to Profile Editor Page if the user hasn't filled out any information yet. */
    if (this.profile.first_name == '') {
      this.router.navigate(['/profile-editor']);
    }

    this.token = `${localStorage.getItem('bearerToken')}`;
  }

  displayToken(): void {
    this.showToken = !this.showToken;
  }

  copyToken(): void {
    navigator.clipboard.writeText(this.token);
    this.snackBar.open('Token Copied', '', { duration: 2000 });
  }

  linkWithGitHub(): void {
    this.profileService.getGitHubOAuthLoginURL().subscribe((url) => {
      window.location.href = url;
    });
  }

  unlinkGitHub() {
    this.profileService.unlinkGitHub().subscribe({
      next: () => (this.profile.github = '')
    });
  }
}
