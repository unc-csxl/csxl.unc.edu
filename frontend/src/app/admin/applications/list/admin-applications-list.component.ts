/**
 * The Admin Application List page retrieves and displays a list of
 * all pending TA application and provides functionality to review them.
 *
 * @author Ben Goulet
 * @copyright 2024
 * @license MIT
 */

import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { Organization } from '../../../organization/organization.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AdminApplicationsService } from '../admin-applications.service';
import { ApplicationReviewModal } from '../widgets/application-review-modal.widget';
import { Application } from '../admin-application.model';
import { Observable } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-admin-applications-list',
  templateUrl: './admin-applications-list.component.html',
  styleUrls: ['./admin-applications-list.component.css']
})
export class AdminApplicationsListComponent {
  /** Application List */
  public organizations$: Observable<Organization[]>;

  public displayedColumns: string[] = ['name'];

  /** Route information to be used in Admin Routing Module */
  public static Route = {
    path: 'applications',
    component: AdminApplicationsListComponent,
    title: 'Application Administration',
    canActivate: [permissionGuard('organization.list', 'organization')]
  };

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private adminApplicationsService: AdminApplicationsService,
    protected applicationReviewDialog: MatDialog
  ) {
    this.organizations$ = adminApplicationsService.organizations$;
    adminApplicationsService.list();
  }

  reviewApplication(selectedApplication: Application): void {
    const dialogRef = this.applicationReviewDialog.open(
      ApplicationReviewModal,
      {
        data: { application: selectedApplication }
      }
    );

    dialogRef.afterClosed().subscribe((result) => {
      console.log('Dialog closed with result:', result);
    });
  }
}
