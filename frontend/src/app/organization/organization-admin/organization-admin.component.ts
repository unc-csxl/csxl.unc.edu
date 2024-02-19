import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { Organization } from '../organization.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AdminOrganizationService } from 'src/app/admin/organization/admin-organization.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-organization-admin',
  templateUrl: './organization-admin.component.html',
  styleUrls: ['./organization-admin.component.css']
})
export class OrganizationAdminComponent {
  /** Organizations List */
  public organizations$: Observable<Organization[]>;

  public displayedColumns: string[] = ['name'];

  /** Route information to be used in Admin Routing Module */
  public static Route = {
    path: 'admin',
    component: OrganizationAdminComponent,
    title: 'Organization Administration',
    canActivate: [permissionGuard('organization.list', 'organization')]
  };

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private organizationAdminService: AdminOrganizationService
  ) {
    this.organizations$ = organizationAdminService.organizations$;
    organizationAdminService.list();
  }

  /** Event handler to open the Organization Editor to edit an existing organization */
  editOrganization(organization: Organization): void {
    this.router.navigate(['organizations', organization.slug, 'edit']);
  }
}
