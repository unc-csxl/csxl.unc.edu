import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { Profile, ProfileService } from '../../profile/profile.service';

@Component({
  selector: 'app-admin-users-roles',
  templateUrl: './admin-accounts.component.html',
  styleUrls: ['./admin-accounts.component.css']
})
export class AdminUsersRolesComponent {
  public profile$: Observable<Profile | undefined>;

  public links = [
    { label: 'Users', path: '/admin/accounts/users', icon: 'group' },
    {
      label: 'Roles',
      path: '/admin/accounts/roles',
      icon: 'admin_panel_settings'
    }
  ];

  constructor(public profileService: ProfileService) {
    this.profile$ = profileService.profile$;
  }
}
