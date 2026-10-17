/**
 * This component is the primary screen for ambassadors at the check-in desk.
 *
 * @author Kris Jordan <kris@cs.unc.edu>, Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023 - 2024
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { PermissionService } from 'src/app/permission.service';

@Component({
  selector: 'app-coworking-ambassador-home',
  templateUrl: './ambassador-home.component.html',
  standalone: false
})
export class AmbassadorPageComponent implements OnInit {
  public links = [
    {
      label: 'XL Reservations',
      path: '/coworking/ambassador/xl',
      icon: 'chair_alt'
    },
    {
      label: 'Room Reservations',
      path: '/coworking/ambassador/room',
      icon: 'meeting_room'
    }
  ];

  public hoursTab = { label: 'Operating Hours', icon: 'schedule' };
  public ambassadorPermission$;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    permission: PermissionService
  ) {
    this.ambassadorPermission$ = permission.check(
      'coworking.reservation.*',
      '*'
    );
  }

  ngOnInit(): void {
    if (!this.route.firstChild) {
      this.router.navigate(['/coworking/ambassador/xl'], { replaceUrl: true });
    }
  }
}
