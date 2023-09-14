/** Home Redirect's user to either About Page (not logged in) or Coworking Page. */

import { Component } from '@angular/core';
import { profileResolver } from '../profile/profile.resolver';
import { ActivatedRoute, Router } from '@angular/router';
import { Profile } from '../models.module';

@Component({
  selector: 'app-home',
  template: ''
})
export class HomeComponent {
  public static Route = {
    path: '',
    component: HomeComponent,
    resolve: { profile: profileResolver }
  }

  constructor(route: ActivatedRoute, router: Router) {
    let profile: Profile | undefined = route.snapshot.data['profile'];
    if (profile) {
      if (profile.id) {
        router.navigateByUrl("/coworking");
      } else {
        router.navigateByUrl("/profile");
      }
    } else {
      router.navigateByUrl("/about");
    }
  }
}
