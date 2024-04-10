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
import { UTANoticeComponent } from 'src/app/ta-application/uta-notice/uta-notice.component';
import { ApplicationsService } from 'src/app/ta-application/ta-application.service';
import { Application } from 'src/app/admin/applications/admin-application.model';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-academics-home',
  templateUrl: './academics-home.component.html',
  styleUrls: ['./academics-home.component.css']
})
export class AcademicsHomeComponent implements OnInit {
  /** Route information to be used in Course Routing Module */
  public static Route = {
    path: '',
    title: 'Academics',
    component: AcademicsHomeComponent,
    canActivate: []
  };

  public user_application$: Observable<Application | null>;
  public new_uta: boolean;

  constructor(
    private gearService: NagivationAdminGearService,
    protected dialog: MatDialog,
    public applicationService: ApplicationsService
  ) {
    this.applicationService.getApplication();
    this.user_application$ = this.applicationService.user_application$;

    this.new_uta = this.applicationService.new_uta;
  }

  onUTAClick(editMode: boolean = false): void {
    const dialogRef = this.dialog.open(UTANoticeComponent, {
      width: '1000px',
      autoFocus: false,
      data: { editMode }
    });

    dialogRef.afterClosed().subscribe();
  }

  ngOnInit() {
    this.gearService.showAdminGear(
      'academics.*',
      '*',
      '',
      'academics/admin/section'
    );
  }
}
