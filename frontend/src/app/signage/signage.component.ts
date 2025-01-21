/**
 * The Signage Component showcases a plethora of useful information for those near the CSXL entrance on the TV.
 *
 * @author Will Zahrt, Andrew Lockard
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  inject,
  OnDestroy,
  OnInit,
  Signal,
  signal,
  WritableSignal
} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { SignageService } from './signage.service';
import { Observable, Subscription, timer, delay } from 'rxjs';
import { fetchWeatherApi } from 'openmeteo';

const REFRESH_FAST_SECONDS = 100000000;
const REFRESH_SLOW_MINUTES = 20;

const params = {
  latitude: 35.910259,
  longitude: -79.055473,
  current: ['temperature_2m', 'weather_code', 'wind_speed_10m'],
  temperature_unit: 'fahrenheit',
  wind_speed_unit: 'mph',
  precipitation_unit: 'inch',
  timezone: 'America/New_York',
  forecast_days: 1
};
const url = 'https://api.open-meteo.com/v1/forecast';

const weather_types: { [weather: string]: string } = {
  sunny: '/assets/sunny.png',
  sunny_windy: '/assets/sunny-windy.png',
  partly_cloudy: '/assets/partly-cloudy.png',
  partly_cloudy_windy: '/assets/partly-cloudy-windy.png',
  rainy: '/assets/rainy.png',
  stormy: '/assets/stormy.png',
  overcast: '/assets/overcast.png',
  snowy: '/assets/snowy.png',
  foggy: '/assets/foggy.png'
};

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
  public weatherData: any; // Store weather data
  private fastSubscription!: Subscription;
  private slowSubscription!: Subscription;
  private dateSubscription!: Subscription;
  public current_weather_icon!: String;

  constructor(protected signageService: SignageService) {}

  // Observable-based method to fetch weather data
  private fetchWeatherData(): Observable<any> {
    return new Observable((observer) => {
      fetchWeatherApi(url, params).then((responses) => {
        const response = responses[0];
        const utcOffsetSeconds = response.utcOffsetSeconds();
        const current = response.current()!;

        // Process the weather data
        this.weatherData = {
          current: {
            time: new Date((Number(current.time()) + utcOffsetSeconds) * 1000),
            temperature2m: current.variables(0)!.value(),
            weatherCode: current.variables(1)!.value(),
            windSpeed10m: current.variables(2)!.value()
          }
        };

        observer.next(this.weatherData); // Emit the data
      });
    });
  }

  private assginWeatherIcon() {
    if (
      this.weatherData.current.weatherCode >= 95 &&
      this.weatherData.current.weatherCode <= 99
    ) {
      this.current_weather_icon = weather_types['stormy'];
    } else if (this.weatherData.current.weatherCode == 3) {
      this.current_weather_icon = weather_types['overcast'];
    } else if (
      this.weatherData.current.weatherCode >= 40 &&
      this.weatherData.current.weatherCode <= 49
    ) {
      this.current_weather_icon = weather_types['foggy'];
    } else if (this.weatherData.current.weatherCode == 2) {
      if (this.weatherData.current.windSpeed10m >= 15) {
        this.current_weather_icon = weather_types['partly_cloudy_windy'];
      } else {
        this.current_weather_icon = weather_types['partly_cloudy'];
      }
    } else if (
      (this.weatherData.current.weatherCode >= 60 &&
        this.weatherData.current.weatherCode <= 66) ||
      (this.weatherData.current.weatherCode >= 80 &&
        this.weatherData.current.weatherCode <= 82)
    ) {
      this.current_weather_icon = weather_types['rainy'];
    } else if (
      (this.weatherData.current.weatherCode >= 70 &&
        this.weatherData.current.weatherCode <= 75) ||
      this.weatherData.current.weatherCode == 85 ||
      this.weatherData.current.weatherCode == 86
    ) {
      this.current_weather_icon = weather_types['snowy'];
    } else if (this.weatherData.current.windSpeed10m >= 15) {
      this.current_weather_icon = weather_types['sunny_windy'];
    } else {
      this.current_weather_icon = weather_types['sunny'];
    }
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
        this.fetchWeatherData().subscribe((data) => {
          this.weatherData = data;
          this.assginWeatherIcon();
          console.log('Weather Data: ', this.weatherData);
        });
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
  }
}
