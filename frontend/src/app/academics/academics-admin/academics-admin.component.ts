import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { Profile } from 'src/app/models.module';
import { ProfileService } from 'src/app/profile/profile.service';

@Component({
  selector: 'app-academics-admin',
  templateUrl: './academics-admin.component.html',
  styleUrls: ['./academics-admin.component.css']
})
export class AcademicsAdminComponent {
  public profile$: Observable<Profile | undefined>;

  public links = [
    { label: 'Terms', path: '/academics/admin/term' },
    { label: 'Courses', path: '/academics/admin/course' },
    { label: 'Sections', path: '/academics/admin/section' },
    { label: 'Rooms', path: '/academics/admin/room' }
  ];

  constructor(public profileService: ProfileService) {
    this.profile$ = profileService.profile$;
  }
}
