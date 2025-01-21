/**
 * The TV Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Will Zahrt
 * @copyright 2024
 * @license MIT
 */

import { HttpClient } from '@angular/common/http';
import { Injectable, OnInit, signal, WritableSignal } from '@angular/core';
import { Observable, map } from 'rxjs';
import {
  FastSignageData,
  FastSignageDataJson,
  SlowSignageData,
  SlowSignageDataJson,
  parseFastSignageDataJson,
  parseSlowSignageDataJson
} from './signage.model';
import { fetchWeatherApi } from 'openmeteo';

const url = 'https://api.open-meteo.com/v1/forecast';
const params = {
  latitude: 35.910259,
  longitude: -79.055473,
  current: ['temperature_2m', 'is_day', 'weather_code', 'wind_speed_10m'],
  temperature_unit: 'fahrenheit',
  wind_speed_unit: 'mph',
  precipitation_unit: 'inch',
  timezone: 'America/New_York',
  forecast_days: 1
};

@Injectable({
  providedIn: 'root'
})
export class SignageService implements OnInit {
  /** Constructor */
  private fastDataSignal: WritableSignal<FastSignageData> = signal({
    active_office_hours: [],
    available_rooms: [],
    seat_availability: []
  });
  public fastData = this.fastDataSignal.asReadonly();

  private slowDataSignal: WritableSignal<SlowSignageData> = signal({
    newest_news: [],
    newest_events: [],
    top_users: [],
    announcement_titles: []
  });
  public slowData = this.slowDataSignal.asReadonly();
  private weatherData: any; // Store weather data to pass to component

  constructor(protected http: HttpClient) {}

  getSlowData() {
    return this.http
      .get<SlowSignageDataJson>(`/api/signage/slow`)
      .pipe(map(parseSlowSignageDataJson))
      .subscribe((slowSignageData) => {
        this.slowDataSignal.set(slowSignageData);
      });
  }

  getFastData() {
    return this.http
      .get<FastSignageDataJson>(`/api/signage/fast`)
      .pipe(map(parseFastSignageDataJson))
      .subscribe((fastSignageData) => {
        this.fastDataSignal.set(fastSignageData);
      });
  }

  // Observable-based method to fetch weather data
  fetchWeatherData(): Observable<any> {
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
            isDay: current.variables(1)!.value(),
            weatherCode: current.variables(2)!.value(),
            windSpeed10m: current.variables(3)!.value()
          }
        };

        observer.next(this.weatherData); // Emit the data
      });
    });
  }

  ngOnInit(): void {
    this.getSlowData();
    this.getFastData();
  }
}
