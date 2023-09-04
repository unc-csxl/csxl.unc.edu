import { Component } from '@angular/core';
import { Route } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';

@Component({
  selector: 'app-coworking-ambassador-page',
  templateUrl: './ambassador-page.component.html',
  styleUrls: ['./ambassador-page.component.css']
})
export class AmbassadorPageComponent {

  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: 'ambassador',
    component: AmbassadorPageComponent,
    title: 'XL Ambassador',
    canActivate: [permissionGuard('coworking.reservation.*', '*')],
    resolve: { profile: profileResolver }
  };

  constructor() {
    console.log("AMB")
  }

}
