/**
 * This experimental component is an admin-level page that allows
 * the developers of the CSXL application to experiment with different
 * designs for future features.
 * 
 * @author Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { Component, HostListener, Inject } from '@angular/core';
import { profileResolver } from '../profile/profile.resolver';
import { Organization } from '../organization/organization.service';
import { Subscription, map } from 'rxjs';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { MAT_DIALOG_DATA, MatDialog, MatDialogRef } from '@angular/material/dialog';
import { EventDetailDialog } from './event-detail-dialog';

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

  sampleOrganization: Organization

  public windowWidth: any;

  constructor(public dialog: MatDialog) {
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
    }
  }

  ngOnInit() {
    this.windowWidth = window.innerWidth;
  }

  @HostListener('window:resize', ['$event'])
  onResize() {
    this.windowWidth = window.innerWidth;
  }

  onEventCardClicked() {
    const MOBILE_SIZE = 680;

    if (this.windowWidth <= MOBILE_SIZE) {
      const dialogRef = this.dialog.open(EventDetailDialog, {
        data: {
          name: "HackNC Hackathon",
          organization: this.sampleOrganization,
          startText: "Oct. 28th, 10:00 AM",
          endText: "Oct. 29th, 10:00 AM",
          location: "Woolen Gym",
          description: "HackNC is a weekend for students of all skill levels to broaden their talents. Your challenge is to make an awesome project in just 24 hours. You will have access to hands-on workshops and demos from our sponsors, as well as exciting talks about the awesome things happening right now with computer science and technology - not to mention all of the free food, shirts, stickers, and swag!",
          requiresPreregistration: true
        },
      });
    }
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
