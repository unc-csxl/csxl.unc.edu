/** Home Redirect's user to either About Page (not logged in) or Coworking Page. */

import { Component } from '@angular/core';
import { profileResolver } from '../profile/profile.resolver';
import { ActivatedRoute, Router } from '@angular/router';

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
    if (route.snapshot.data['profile']) {
      router.navigateByUrl("/coworking")
    } else {
      router.navigateByUrl("/about");
    }
  }
}
