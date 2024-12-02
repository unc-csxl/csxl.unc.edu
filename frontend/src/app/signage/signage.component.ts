/**
 * The Signage Component showcases a plethora of useful information for those near the CSXL entrance on the TV.
 *
 * @author WilL Zahrt, Andrew Lockard
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  OnDestroy,
  OnInit,
  Signal,
  signal,
  WritableSignal
} from '@angular/core';
import { SignageService } from './signage.service';
import { FastSignageData, SlowSignageData } from './signage.model';
import { Subscription, timer } from 'rxjs';

const REFRESH_FAST_SECONDS = 100000000;
const REFRESH_SLOW_MINUTES = 20;

@Component({
  selector: 'app-signage',
  templateUrl: './signage.component.html',
  styleUrl: './signage.component.css'
})
export class SignageComponent implements OnInit, OnDestroy {
  public static Route = {
    path: '',
    component: SignageComponent
  };

  date: number = Date.now();

  private fastSubscription!: Subscription;
  private slowSubscription!: Subscription;

  constructor(protected signageService: SignageService) {
  }

  ngOnInit(): void {
    this.fastSubscription = timer(0, REFRESH_FAST_SECONDS * 1000).subscribe(
      () => {
        this.signageService.getFastData();
      }
    );

    this.slowSubscription = timer(0, REFRESH_SLOW_MINUTES * 60000).subscribe(
      () => {
        this.signageService.getSlowData();
      }
    );
  }

  ngOnDestroy(): void {
    if (this.fastSubscription) {
      // If statements needed here to prevent null exception
      this.fastSubscription.unsubscribe();
    }
    if (this.slowSubscription) {
      this.slowSubscription.unsubscribe();
    }
  }
}
