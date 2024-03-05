import { Component, OnDestroy, OnInit } from '@angular/core';
import { Route } from '@angular/router';
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
export class AmbassadorPageComponent {
  public links = [
    { label: 'XL Reservations', path: '/coworking/ambassador/xl' },
    { label: 'Room Reservations', path: '/coworking/ambassador/room' }
  ];

  constructor(public ambassadorService: AmbassadorService) {}
}
