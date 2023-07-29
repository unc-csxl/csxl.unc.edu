import { Component } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';

@Component({
  selector: 'app-coworking-page',
  templateUrl: './coworking-page.component.html',
  styleUrls: ['./coworking-page.component.css']
})
export class CoworkingPageComponent {

  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: 'coworking',
    component: CoworkingPageComponent,
    title: 'Coworking',
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  constructor(route: ActivatedRoute, private router: Router) { }
}
