/**
 * The Academics homepage serves as the hub for all academic features
 * for students in the CSXL community.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';
import { Router } from '@angular/router';

@Component({
    selector: 'app-academics-home',
    templateUrl: './academics-home.component.html',
    styleUrls: ['./academics-home.component.css'],
    standalone: false
})
export class AcademicsHomeComponent implements OnInit {
  /** Route information to be used in Course Routing Module */
  public static Route = {
    path: '',
    title: 'Academics',
    component: AcademicsHomeComponent,
    canActivate: []
  };

  constructor(
    private gearService: NagivationAdminGearService,
    protected dialog: MatDialog,
    private router: Router
  ) {}

  ngOnInit() {
    this.gearService.showAdminGearByPermissionCheck(
      'academics.*',
      '*',
      '',
      'academics/admin/section'
    );
  }
}
