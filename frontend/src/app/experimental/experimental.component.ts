/**
 * This experimental component is an admin-level page that allows
 * the developers of the CSXL application to experiment with different
 * designs for future features.
 * 
 * @author Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { Component } from '@angular/core';
import { profileResolver } from '../profile/profile.resolver';
import { Organization } from '../organization/organization.service';

@Component({
  selector: 'app-experimental',
  templateUrl: './experimental.component.html',
  styleUrls: ['./experimental.component.css']
})
export class ExperimentalComponent {

  /** Route information to be used in App Routing Module */
  public static Route = {
    path: '',
    title: 'Experimental - Events',
    component: ExperimentalComponent,
    canActivate: [],
    resolve: { profile: profileResolver }
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
