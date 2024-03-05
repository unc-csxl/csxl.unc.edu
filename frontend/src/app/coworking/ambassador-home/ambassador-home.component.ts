/**
 * This component is the primary screen for ambassadors at the check-in desk.
 *
 * @author Kris Jordan <kris@cs.unc.edu>
 * @copyright 2023 - 2024
 * @license MIT
 */

import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-coworking-ambassador-home',
  templateUrl: './ambassador-home.component.html',
  styleUrls: ['./ambassador-home.component.css']
})
export class AmbassadorPageComponent implements OnInit {
  public links = [
    {
      label: 'XL Reservations',
      path: '/coworking/ambassador/xl',
      default: true
    },
    { label: 'Room Reservations', path: '/coworking/ambassador/room' }
  ];

  constructor(private router: Router) {}

  ngOnInit(): void {
    // Find the default link and navigate to it
    const defaultLink = this.links.find((link) => link.default);
    if (defaultLink) {
      this.router.navigate([defaultLink.path]);
    }
  }
}
