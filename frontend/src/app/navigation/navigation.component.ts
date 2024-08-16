import { Component, OnDestroy, OnInit } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable, Subscription } from 'rxjs';
import { filter, map } from 'rxjs/operators';
import { NavigationService as NavigationTitleService } from './navigation.service';
import { MatDialog } from '@angular/material/dialog';
import { ErrorDialogComponent } from './error-dialog/error-dialog.component';
import { MatSidenav } from '@angular/material/sidenav';
import { AuthenticationService } from '../authentication.service';
import { Router, RouterEvent } from '@angular/router';
import { Profile, ProfileService } from '../profile/profile.service';
import { PermissionService } from '../permission.service';
import { NagivationAdminGearService } from './navigation-admin-gear.service';
import { SlackInviteBox } from './widgets/slack-invite-box/slack-invite-box.widget';
import { SocialMediaIconWidgetService } from '../shared/social-media-icon/social-media-icon.widget.service';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.css']
})
export class NavigationComponent implements OnInit, OnDestroy {
  private errorDialogSubscription!: Subscription;

  public isHandset: boolean = false;
  private isHandsetSubscription!: Subscription;

  public profile$: Observable<Profile | undefined>;
  public checkinPermission$: Observable<boolean>;
  public adminPermission$: Observable<boolean>;
  public ambassadorPermission$: Observable<boolean>;
  public hiringPermission$: Observable<boolean>;

  constructor(
    public auth: AuthenticationService,
    public router: Router,
    protected permission: PermissionService,
    private profileService: ProfileService,
    private breakpointObserver: BreakpointObserver,
    protected navigationService: NavigationTitleService,
    protected navigationAdminGearService: NagivationAdminGearService,
    protected errorDialog: MatDialog,
    protected slackDialog: MatDialog,
    protected iconService: SocialMediaIconWidgetService
  ) {
    this.profile$ = this.profileService.profile$;
    this.checkinPermission$ = this.permission.check(
      'checkin.create',
      'checkin/'
    );
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');
    this.ambassadorPermission$ = this.permission.check(
      'coworking.reservation.*',
      '*'
    );
    this.hiringPermission$ = this.permission.check('hiring.*', '*');
    // Reset the admin settings navigation every time the route changes
    router.events
      .pipe(filter((e) => e instanceof RouterEvent))
      .subscribe((_) => {
        navigationAdminGearService.resetAdminSettingsNavigation();
      });
  }

  ngOnInit(): void {
    this.errorDialogSubscription = this.initErrorDialog();
    this.isHandsetSubscription = this.initResponsiveMenu();
  }

  ngOnDestroy(): void {
    this.errorDialogSubscription.unsubscribe();
    this.isHandsetSubscription.unsubscribe();
  }

  hideMobileSidenav(nav: MatSidenav): void {
    if (this.isHandset) {
      nav.close();
    }
  }

  onSlackInviteClick(): void {
    const dialogRef = this.slackDialog.open(SlackInviteBox, {
      autoFocus: 'dialog'
    });
    dialogRef.afterClosed().subscribe();
  }

  private initErrorDialog() {
    return this.navigationService.error$.subscribe((message) => {
      if (message !== null) {
        this.errorDialog.open(ErrorDialogComponent, { data: { message } });
      }
    });
  }

  private initResponsiveMenu() {
    return this.breakpointObserver
      .observe(Breakpoints.HandsetPortrait)
      .pipe(map((result) => result.matches))
      .subscribe((isHandset) => (this.isHandset = isHandset));
  }

  openLink(link: string) {
    window.open(link ?? '', '_blank');
  }
}
