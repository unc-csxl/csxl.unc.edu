/**
 * The Coworking Admin Component provides the functionality for managing operating hours
 *
 * @author David Foss, Ella Gonzales, Francine Wei, Tobenna Okoli
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  WritableSignal,
  OnInit,
  OnDestroy,
  signal,
  effect,
  inject,
  ViewChild
} from '@angular/core';
import { permissionGuard } from 'src/app/permission.guard';
import { OperatingHours } from '../coworking.models';
import { currentTermResolver } from 'src/app/academics/academics.resolver';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { MatDialog } from '@angular/material/dialog';
import { OperatingHoursMobileEditorDialog } from './coworking-operating-hours-mobile-dialog/coworking-operating-hours-mobile.dialog';
import { OperatingHoursCalendar } from 'src/app/shared/operating-hours-calendar/operating-hours-calendar.widget';

@Component({
  selector: 'app-coworking-admin',
  templateUrl: './coworking-admin.component.html',
  styleUrls: ['./coworking-admin.component.css']
})
export class CoworkingAdminComponent implements OnInit, OnDestroy {
  @ViewChild('calendar') calendar!: OperatingHoursCalendar;
  isAddingHours: WritableSignal<boolean> = signal(false);
  selectedOperatingHours: WritableSignal<OperatingHours | null> = signal(null);
  isPortrait: boolean = false;

  constructor(protected dialog: MatDialog) {
    inject(BreakpointObserver)
      .observe([Breakpoints.HandsetPortrait])
      .subscribe((result) => {
        this.isPortrait = result.matches;
      });
  }

  public static Route = {
    path: 'admin',
    component: CoworkingAdminComponent,
    title: 'CSXL Open Hours Administration',
    canActivate: [permissionGuard('coworking.operating_hours', '*')],
    resolve: {
      currentTerm: currentTermResolver
    }
  };
  /** Shows the editor for adding Operating Hours
   *
   * On desktop, it will display as a side panel
   * On mobile, it will display as a dialog box
   *
   * On desktop, this action is persisted across reloads.
   *
   * @returns {void}
   *
   */
  showAddHoursPanel(): void {
    this.selectedOperatingHours.set(null);
    if (this.isPortrait) {
      this.dialog.open(OperatingHoursMobileEditorDialog, {
        height: '550px',
        width: '300px',
        data: {
          selectedOperatingHours: this.selectedOperatingHours,
          calendar: this.calendar
        }
      });
    } else {
      this.isAddingHours.set(true);
      sessionStorage.setItem('isAddingHours', String(this.isAddingHours()));
    }
  }

  /**
   * Select a given operating hours instance
   *
   * @param {OperatingHours} operatingHours - The operating hours to select
   *
   * @returns {void}
   */
  selectOperatingHours(operatingHours: OperatingHours): void {
    this.selectedOperatingHours.set(operatingHours);
    if (this.isPortrait) {
      this.dialog.open(OperatingHoursMobileEditorDialog, {
        height: '550px', // Doing 550px specifically so that all content is visible unless recurring, in which case one element will be partially visible
        width: '300px',
        data: {
          selectedOperatingHours: this.selectedOperatingHours,
          calendar: this.calendar
        }
      });
    } else {
      this.isAddingHours.set(false);
      sessionStorage.removeItem('isAddingHours');
    }
  }

  ngOnInit(): void {
    // Open the add hours dialog if it is remembered that we were adding hours
    const savedVisibility = sessionStorage.getItem('isAddingHours');
    this.isAddingHours.set(savedVisibility === 'true');
  }

  ngOnDestroy(): void {
    // Clear memory of if we were adding hours when we navigate to another page within the CSXL
    sessionStorage.removeItem('isAddingHours');
  }
}
