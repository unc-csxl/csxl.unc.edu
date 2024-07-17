/**
 * This component is the primary screen for ambassadors at the check-in desk.
 *
 * @author Kris Jordan <kris@cs.unc.edu>, Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023 - 2024
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
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
      icon: 'chair_alt'
    },
    {
      label: 'Room Reservations',
      path: '/coworking/ambassador/room',
      icon: 'meeting_room'
    }
  ];

  constructor(private router: Router) {}

  ngOnInit(): void {
    // Find the default link and navigate to it
    this.router.navigate(['/coworking/ambassador/xl']);
  }
}
