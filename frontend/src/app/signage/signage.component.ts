/**
 * The Signage Component showcases a plethora of useful information for those near the CSXL entrance on the TV.
 *
 * @author Will Zahrt, Andrew Lockard
 * @copyright 2024
 * @license MIT
 */

import { Component, OnDestroy, OnInit } from '@angular/core';
import { SignageService } from './signage.service';
import { Subscription, timer, delay } from 'rxjs';
import { WeatherData } from './signage.model';

const REFRESH_FAST_SECONDS = 20;
const REFRESH_SLOW_MINUTES = 20;

const weather_types: { [weather: string]: string } = {
  sunny: '/assets/sunny.png',
  sunny_windy: '/assets/sunny-windy.png',
  partly_cloudy: '/assets/partly-cloudy.png',
  partly_cloudy_windy: '/assets/partly-cloudy-windy.png',
  rainy: '/assets/rainy.png',
  stormy: '/assets/stormy.png',
  overcast: '/assets/overcast.png',
  snowy: '/assets/snowy.png',
  foggy: '/assets/foggy.png',
  night: '/assets/night.png'
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
  private fastSubscription!: Subscription;
  private slowSubscription!: Subscription;
  private dateSubscription!: Subscription;
  private weatherSubscription!: Subscription;

  constructor(protected signageService: SignageService) {}

  /**
   * Weather icons are assigned based on WMO Weather Codes.
   *
   * Here is a table showing all of them:
   *
   * https://www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/HTML/WMO-CODE/WMO4677.HTM
   *
   * @param weatherData The weather data retrieved from Open-Meteo.
   * @return The path to the correct .png weather icon.
   */
  public assignWeatherIcon(weatherData: WeatherData): string {
    if (weatherData.weatherCode >= 95 && weatherData.weatherCode <= 99) {
      // Codes 95-99 indicate thunderstorms.
      return weather_types['stormy'];
    } else if (weatherData.weatherCode == 3) {
      // Code 3 indicates overcast clouds.
      return weather_types['overcast'];
    } else if (weatherData.weatherCode >= 40 && weatherData.weatherCode <= 49) {
      // Codes 40-49 indicate fog.
      return weather_types['foggy'];
    } else if (
      (weatherData.weatherCode >= 60 && weatherData.weatherCode <= 66) ||
      (weatherData.weatherCode >= 80 && weatherData.weatherCode <= 82)
    ) {
      // Codes 60-66 indicate non-freezing rain.
      // Codes 80-82 indicate different rain shower types.
      return weather_types['rainy'];
    } else if (
      (weatherData.weatherCode >= 70 && weatherData.weatherCode <= 75) ||
      weatherData.weatherCode == 85 ||
      weatherData.weatherCode == 86
    ) {
      // Codes 70-75 indicate snowflake fall.
      // Codes 85-86 indicate snow showers.
      return weather_types['snowy'];
    } else if (weatherData.isDay == 0) {
      // isDay == 0 indicates night time.
      return weather_types['night'];
    } else if (weatherData.weatherCode == 2) {
      // Code 2 indicates partly cloudy.
      if (weatherData.windSpeed10m >= 15) {
        return weather_types['partly_cloudy_windy'];
      } else {
        return weather_types['partly_cloudy'];
      }
    } else if (weatherData.windSpeed10m >= 15) {
      return weather_types['sunny_windy'];
    } else {
      // Default to sunny weather icon.
      return weather_types['sunny'];
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
      }
    );

    this.weatherSubscription = timer(0, REFRESH_SLOW_MINUTES * 60000).subscribe(
      () => {
        this.signageService.fetchWeatherData();
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
