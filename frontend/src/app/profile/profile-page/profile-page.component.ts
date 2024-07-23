/**
 * The Profile Page displays information about the user.
 *
 * @author Jade Keegan, Aziz Al-Shayef
 * @copyright 2024
 * @license MIT
 */

import { Component } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from '../profile.resolver';
import { Profile, ProfileService } from '../profile.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { CommunityAgreement } from 'src/app/shared/community-agreement/community-agreement.widget';
import { AuthenticationService } from 'src/app/authentication.service';
import { SocialMediaIconWidgetService } from 'src/app/shared/social-media-icon/social-media-icon.widget.service';

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

  /** Bearer Token Fields */
  public token: string;
  public showToken: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public auth: AuthenticationService,
    protected profileService: ProfileService,
    protected snackBar: MatSnackBar,
    protected dialog: MatDialog,
    private icons: SocialMediaIconWidgetService
  ) {
    /** Get currently-logged-in user. */
    const data = this.route.snapshot.data as {
      profile: Profile;
    };
    this.profile = data.profile;

    /** Switch to Profile Editor Page if the user hasn't saved their information yet. */
    if (this.profile.first_name == '') {
      this.router.navigate(['/profile/edit']);
    }

    /** Get bearer token from local storage. */
    this.token = `${localStorage.getItem('bearerToken')}`;
  }

  /** Display Bearer Token */
  displayToken(): void {
    this.showToken = !this.showToken;
  }

  /** Copy Bearer Token to Clipboard */
  copyToken(): void {
    navigator.clipboard.writeText(this.token);
    this.snackBar.open('Token Copied', '', { duration: 2000 });
  }

  /** Go to GitHub authorization page to link account to GH. */
  linkWithGitHub(): void {
    this.profileService.getGitHubOAuthLoginURL().subscribe((url) => {
      window.location.href = url;
    });
  }

  /** Remove GitHub connection. */
  unlinkGitHub() {
    this.profileService.unlinkGitHub().subscribe({
      next: () => (this.profile.github = '')
    });
  }

  /** Open Community Agreement Dialog */
  openAgreementDialog(): void {
    const dialogRef = this.dialog.open(CommunityAgreement, {
      width: '1000px',
      height: '800px'
    });
    this.profileService.profile$.subscribe();
    dialogRef.afterClosed().subscribe();
  }
}
