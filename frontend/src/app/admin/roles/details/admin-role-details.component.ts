import { Component, inject, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatAutocompleteActivatedEvent, MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { ActivatedRoute, ActivatedRouteSnapshot, Router } from '@angular/router';
import { debounceTime, filter, mergeMap, Observable, of, ReplaySubject, startWith } from 'rxjs';
import { permissionGuard } from 'src/app/permission.guard';
import { Permission, Profile, ProfileService } from 'src/app/profile/profile.service';
import { RoleDetails } from 'src/app/role';
import { RoleAdminService } from '../role-admin.service';

@Component({
    selector: 'app-admin-role-details',
    templateUrl: './admin-role-details.component.html',
    styleUrls: ['./admin-role-details.component.css']
})
export class AdminRoleDetailsComponent implements OnInit {

    public role: RoleDetails;

    public grantPermissionForm: Permission = {
        action: '',
        resource: ''
    };

    public userLookup: FormControl = new FormControl();
    private filteredUsers: ReplaySubject<Profile[]> = new ReplaySubject();
    public filteredUsers$: Observable<Profile[]> = this.filteredUsers.asObservable();
    public selectedUser?: Profile;

    public static Route = {
        path: 'roles/:id',
        component: AdminRoleDetailsComponent,
        title: 'Role Administration',
        canActivate: [permissionGuard('role.details', 'role/{id}')],
        resolve: { 
            role: (route: ActivatedRouteSnapshot) => {
                const id = parseInt(route.paramMap.get('id')!);
                return inject(RoleAdminService).details(id); 
            }
        }
    }

    constructor(
        private roleAdminService: RoleAdminService,
        private profileService: ProfileService,
        private router: Router,
        route: ActivatedRoute,
    ) {
        let data = route.snapshot.data as { role: RoleDetails };
        this.role = data.role;
    }

    public ngOnInit() {
        this.filteredUsers$ = this.userLookup.valueChanges.pipe(
            startWith(''),
            filter((search: string) => search.length > 2),
            debounceTime(100),
            mergeMap((search) => this.profileService.search(search))
        );
    }

    public onGrantPermission() {
        if (this.grantPermissionForm.action === '' || this.grantPermissionForm.resource === '') {
            return;
        }
        this.roleAdminService.grant(this.role.id, this.grantPermissionForm).subscribe((role: RoleDetails) => {
            this.role = role;
            this.grantPermissionForm = { action: '', resource: '' };
        });
    }

    public onRevokePermission(permission: Permission) {
        this.roleAdminService.revoke(this.role.id, permission.id!).subscribe(() => {
            this.role.permissions = this.role.permissions.filter(p => p !== permission);
        });
    }

    public onOptionSelected(event: MatAutocompleteSelectedEvent) {
        let user = event.option.value as Profile;
        this.selectedUser = user;
        this.userLookup.setValue('');
    }

    public onAddMember() {
        if (!this.selectedUser) { return; }
        this.roleAdminService.add(this.role.id, this.selectedUser).subscribe((role: RoleDetails) => {
            this.role = role;
            this.selectedUser = undefined;
        })
    }

    public changeSelectedMember() {
        this.selectedUser = undefined;
        this.userLookup.setValue('');
    }

    public onRemoveMember(user: Profile) {
        this.roleAdminService.remove(this.role.id, user.id!).subscribe(() => {
            this.role.users = this.role.users.filter(u => u !== user);
        });
    }

}