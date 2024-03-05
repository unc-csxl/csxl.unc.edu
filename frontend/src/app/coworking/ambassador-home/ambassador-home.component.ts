import { Component, OnDestroy, OnInit } from '@angular/core';
import { Route, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Observable, Subscription, map, mergeMap, tap, timer } from 'rxjs';
import { Reservation } from '../coworking.models';
import { AmbassadorService } from './ambassador.service';

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

  constructor(
    public ambassadorService: AmbassadorService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Find the default link and navigate to it
    const defaultLink = this.links.find((link) => link.default);
    if (defaultLink) {
      this.router.navigate([defaultLink.path]);
    }
  }
}
