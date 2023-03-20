import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { Profile, ProfileService } from '../profile/profile.service';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: []
})
export class AdminComponent implements OnInit {

  public profile$: Observable<Profile | undefined>;

  public links = [
    { label: 'Users', path: '/admin/users' },
    { label: 'Roles', path: '/admin/roles' },
    { label: 'Checkins', path: '/admin/checkins' },
  ];

  constructor(public profileService: ProfileService) {
    this.profile$ = profileService.profile$;
  }

  ngOnInit(): void {}

}