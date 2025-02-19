/**
 * The TV Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Will Zahrt
 * @author Andrew Lockard
 * @copyright 2024
 * @license MIT
 */

import { HttpClient } from '@angular/common/http';
import { Injectable, signal, WritableSignal } from '@angular/core';
import { map } from 'rxjs';
import {
  FastSignageData,
  FastSignageDataJSON,
  SlowSignageData,
  SlowSignageDataJSON,
  WeatherData,
  parseFastSignageDataJSON,
  parseSlowSignageDataJSON
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
export class SignageService {
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
    announcements: []
  });
  public slowData = this.slowDataSignal.asReadonly();

  private weatherDataSignal: WritableSignal<WeatherData> = signal({
    temperature2m: 100,
    isDay: 1,
    weatherCode: 0,
    windSpeed10m: 0
  });
  public weatherData = this.weatherDataSignal.asReadonly();

  constructor(protected http: HttpClient) {
    this.getSlowData();
    this.getFastData();
    this.fetchWeatherData();
  }

  /**
   * Fetches the slow data from the backend, parses the JSON into the frontend model, and updates the signals
   *
   * @returns SlowData Subscription
   */
  getSlowData() {
    return this.http
      .get<SlowSignageDataJSON>(`/api/signage/slow`)
      .pipe(map(parseSlowSignageDataJSON))
      .subscribe((slowSignageData) => {
        this.slowDataSignal.set(slowSignageData);
      });
  }

  /**
   * Fetches the fast data from the backend, parses JSON into frontend model, and updates fast data signal
   *
   * @returns FastData Subscription
   */
  getFastData() {
    return this.http
      .get<FastSignageDataJSON>(`/api/signage/fast`)
      .pipe(map(parseFastSignageDataJSON))
      .subscribe((fastSignageData) => {
        this.fastDataSignal.set(fastSignageData);
      });
  }

  /**
   * Fetches weather data from open mateo using params defined above, and updates the weather signal
   *
   * Gets the temperature, day/night distinction, weather code (cloudy/rainy/etc.), and wind speed for Sitterson Hall
   */
  fetchWeatherData() {
    fetchWeatherApi(url, params).then((responses) => {
      const response = responses[0];
      const current = response.current()!;

      // Process the weather data
      this.weatherDataSignal.set({
        temperature2m: current.variables(0)!.value(),
        isDay: current.variables(1)!.value(),
        weatherCode: current.variables(2)!.value(),
        windSpeed10m: current.variables(3)!.value()
      });
    });
  }
}
