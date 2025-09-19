/**
 * The Signage Component showcases a plethora of useful information for those near the CSXL entrance on the TV.
 *
 * @author Will Zahrt, Andrew Lockard
 * @copyright 2024
 * @license MIT
 */

import { Component, OnDestroy, OnInit } from '@angular/core';
import { SignageService } from './signage.service';
import { WeatherService } from './weather.service';
import { Subscription, timer, delay } from 'rxjs';

const REFRESH_FAST_SECONDS = 20;
const REFRESH_SLOW_MINUTES = 20;

@Component({
    selector: 'app-signage',
    templateUrl: './signage.component.html',
    styleUrl: './signage.component.css',
    standalone: false
})
export class SignageComponent implements OnInit, OnDestroy {
  public static Route = {
    path: '',
    component: SignageComponent
  };

  date: number = Date.now();
  private fastSubscription!: Subscription;
  private slowSubscription!: Subscription;
  private dateSubscription!: Subscription;
  private weatherSubscription!: Subscription;

  constructor(
    protected signageService: SignageService,
    protected weatherService: WeatherService
  ) {}

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

    this.weatherSubscription = timer(0, REFRESH_SLOW_MINUTES * 60000).subscribe(
      () => {
        this.weatherService.fetchWeatherData();
      }
    );

    // Delay the observable emission so the clock updates on the minute
    this.dateSubscription = timer(0, 60000)
      .pipe(delay(60000 - (Date.now() % 60000)))
      .subscribe(() => {
        this.date = Date.now();
      });
  }

  ngOnDestroy(): void {
    // If statements needed here to prevent null exception
    if (this.fastSubscription) {
      this.fastSubscription.unsubscribe();
    }
    if (this.slowSubscription) {
      this.slowSubscription.unsubscribe();
    }
    if (this.dateSubscription) {
      this.dateSubscription.unsubscribe();
    }

    if (this.weatherSubscription) {
      this.weatherSubscription.unsubscribe();
    }
  }
}
