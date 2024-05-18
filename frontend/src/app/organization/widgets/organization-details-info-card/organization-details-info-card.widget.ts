/**
 * The Organization Details Info Card widget abstracts the implementation of each
 * individual organization detail card from the whole organization detail page.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component, Input, OnDestroy, OnInit, input } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Subscription } from 'rxjs';
import { map } from 'rxjs/operators';
import { Organization } from '../../organization.model';
import { Profile } from 'src/app/profile/profile.service';
import { PermissionService } from 'src/app/permission.service';
import { Observable } from 'rxjs';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';

@Component({
  selector: 'organization-details-info-card',
  templateUrl: './organization-details-info-card.widget.html',
  styleUrls: ['./organization-details-info-card.widget.css']
})
export class OrganizationDetailsInfoCard implements OnInit, OnDestroy {
  /** The organization to show */
  @Input() organization: Organization | undefined;
  /** The currently logged in user */
  @Input() profile?: Profile;

  /** Holds data on whether or not the user is on a mobile device */
  public isHandset: boolean = false;
  private isHandsetSubscription!: Subscription;

  /** Holds data on whether or not the user is on a tablet */
  public isTablet: boolean = false;
  private isTabletSubscription!: Subscription;

  /** Constructs the organization detail info card widget */
  constructor(
    private breakpointObserver: BreakpointObserver,
    private gearService: NagivationAdminGearService
  ) {}

  /** Runs whenever the view is rendered initally on the screen */
  ngOnInit(): void {
    this.isHandsetSubscription = this.initHandset();
    this.isTabletSubscription = this.initTablet();
    this.gearService.showAdminGearByPermissionCheck(
      'organization.*',
      `organization/${this.organization?.slug}`,
      '',
      `organizations/${this.organization?.slug}/edit`
    );
  }

  /** Unsubscribe from subscribers when the page is destroyed */
  ngOnDestroy(): void {
    this.isHandsetSubscription.unsubscribe();
    this.isTabletSubscription.unsubscribe();
  }

  /** Determines whether the page is being used on a mobile device */
  private initHandset() {
    return this.breakpointObserver
      .observe([Breakpoints.Handset, Breakpoints.TabletPortrait])
      .pipe(map((result) => result.matches))
      .subscribe((isHandset) => (this.isHandset = isHandset));
  }

  /** Determines whether the page is being used on a tablet */
  private initTablet() {
    return this.breakpointObserver
      .observe(Breakpoints.TabletLandscape)
      .pipe(map((result) => result.matches))
      .subscribe((isTablet) => (this.isTablet = isTablet));
  }
}
