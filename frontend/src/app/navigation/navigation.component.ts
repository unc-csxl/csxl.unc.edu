import { Component, OnDestroy, OnInit } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Subscription } from 'rxjs';
import { map } from 'rxjs/operators';
import { NavigationService as NavigationTitleService } from './navigation.service';
import { MatDialog } from '@angular/material/dialog';
import { ErrorDialogComponent } from './error-dialog/error-dialog.component';
import { MatSidenav } from '@angular/material/sidenav';
import { AuthenticationService } from '../authentication/authentication.service';
import { Router } from '@angular/router';
import { Profile, ProfileService, Role } from '../profile/profile.service';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.css']
})
export class NavigationComponent implements OnInit, OnDestroy {

  public Role: typeof Role = Role;

  private errorDialogSubscription!: Subscription;

  public isHandset: boolean = false;
  private isHandsetSubscription!: Subscription;

  public profile?: Profile;
  private profileSubscription!: Subscription;

  constructor(
    public auth: AuthenticationService,
    public router: Router,
    public profileService: ProfileService,
    private breakpointObserver: BreakpointObserver,
    protected navigationService: NavigationTitleService,
    protected errorDialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.errorDialogSubscription = this.initErrorDialog();
    this.isHandsetSubscription = this.initResponsiveMenu();
    this.profileSubscription = this.initProfile();
  }

  ngOnDestroy(): void {
    this.errorDialogSubscription.unsubscribe();
    this.isHandsetSubscription.unsubscribe();
    this.profileSubscription.unsubscribe();
  }

  hideMobileSidenav(nav: MatSidenav): void {
    if (this.isHandset) {
      nav.close();
    }
  }

  private initErrorDialog() {
    return this.navigationService.error$.subscribe(
      (message) => {
        if (message !== null) {
          this.errorDialog.open(ErrorDialogComponent, { data: { message } });
        }
      }
    );
  }

  private initResponsiveMenu() {
    return this.breakpointObserver
        .observe(Breakpoints.HandsetPortrait)
        .pipe(map(result => result.matches))
        .subscribe(isHandset => this.isHandset = isHandset);
  }

  private initProfile() {
    return this.profileService.profile$.subscribe(profile => this.profile = profile);
  }

}