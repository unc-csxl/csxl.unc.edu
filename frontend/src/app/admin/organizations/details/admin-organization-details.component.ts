/** Constructs the Admin Organization Details page and stores/retrieves any necessary data for it. */

import { Component, inject, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { ActivatedRoute, ActivatedRouteSnapshot, Router } from '@angular/router';
import { debounceTime, filter, mergeMap, Observable, of, ReplaySubject, startWith } from 'rxjs';
import { permissionGuard } from 'src/app/permission.guard';
import { ProfileService } from 'src/app/profile/profile.service';
import { Organization, OrgRole, Profile } from 'src/app/models.module';
import { OrganizationsAdminService } from '../organizations-admin.service';

@Component({
    selector: 'app-admin-organization-details',
    templateUrl: './admin-organization-details.component.html',
    styleUrls: ['./admin-organization-details.component.css']
})
export class AdminOrganizationDetailsComponent implements OnInit {

    // Current Organization
    public organization: Organization;

    // User Lookup Form Data
    public userLookup: FormControl = new FormControl();
    private filteredUsers: ReplaySubject<Profile[]> = new ReplaySubject();
    public filteredUsers$: Observable<Profile[]> = this.filteredUsers.asObservable();
    public selectedUser?: Profile;

    /** Route information to be used in Admin Routing Module */
    public static Route = {
        path: 'organizations/:id',
        component: AdminOrganizationDetailsComponent,
        title: 'Organization Administration',
        canActivate: [permissionGuard('organizations.details', 'organizations/{id}')],
        resolve: {
            organization: (route: ActivatedRouteSnapshot) => {
                const id = parseInt(route.paramMap.get('id')!);
                return inject(OrganizationsAdminService).details(id);
            }
        }
    }

    constructor(
        private organizationsAdminService: OrganizationsAdminService,
        private profileService: ProfileService,
        private router: Router,
        route: ActivatedRoute,
    ) {
        let data = route.snapshot.data as { organization: Organization };
        this.organization = data.organization;
    }

    public ngOnInit() {
        this.filteredUsers$ = this.userLookup.valueChanges.pipe(
            startWith(''),
            filter((search: string) => search.length > 2),
            debounceTime(100),
            mergeMap((search) => this.profileService.search(search))
        );
    }

    public onOptionSelected = (event: MatAutocompleteSelectedEvent) => {
        let user = event.option.value as Profile;
        this.selectedUser = user;
        this.userLookup.setValue('');
    }

    public changeSelectedMember = () => {
        this.selectedUser = undefined;
        this.userLookup.setValue('');
    }

    /** Returns a list of OrgRoles representing the Organization's Managers
     * @returns {OrgRole[]}
     */
    public getOrgManagers = () => {
        // Filter the organization's OrgRoles for only manager roles
        return this.organization.user_associations.filter((association) => association.membership_type >= 2);
    }

    /** Event handler for adding a manager to the organization */
    public onAddManager = () => {
        if (!this.selectedUser) { return; }
        // Add the manager based on the selectedUser (from the form) and the current organization id
        this.organizationsAdminService.addAdmin(this.selectedUser, this.organization)
            .subscribe((org_role: OrgRole) => {
                // Update the organization in the component
                this.organizationsAdminService.details(org_role.org_id).subscribe(org => this.organization = org);
                this.selectedUser = undefined;
            })
    }

    /** Event handler for removing a manager from the organization 
     * @param org_role: a valid OrgRole model representing the role (manager) to remove from the organization
    */
    public onRemoveManager = (org_role: OrgRole) => {
        this.organizationsAdminService.removeManager(org_role).subscribe(() => {
            this.organizationsAdminService.details(org_role.org_id).subscribe(org => this.organization = org);
        });
    }

    /** Event handler for deleting an organization
     * @param org_id: id of the organization you want to delete
    */
    deleteOrganization = (org_id: number) => {
        this.organizationsAdminService.deleteOrganization(org_id).subscribe(() => console.log('Delete successful.'));

        // Navigate back to list of orgs.
        this.router.navigate(['/admin/organizations']).then(() => location.reload());
    }
}