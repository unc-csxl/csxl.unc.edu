/**
 * The Weather Service abstracts weather API calls from the components.
 *
 * @author Will Zahrt
 * @copyright 2025
 * @license MIT
 */

import { HttpClient } from '@angular/common/http';
import { Injectable, signal, WritableSignal } from '@angular/core';
import { WeatherData } from './signage.model';
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

const weather_types: { [weather: string]: string } = {
  sunny: '/assets/weather-icons/sunny.png',
  sunny_windy: '/assets/weather-icons/sunny-windy.png',
  partly_cloudy: '/assets/weather-icons/partly-cloudy.png',
  partly_cloudy_windy: '/assets/weather-icons/partly-cloudy-windy.png',
  rainy: '/assets/weather-icons/rainy.png',
  stormy: '/assets/weather-icons/stormy.png',
  overcast: '/assets/weather-icons/overcast.png',
  snowy: '/assets/weather-icons/snowy.png',
  foggy: '/assets/weather-icons/foggy.png',
  night: '/assets/weather-icons/night.png'
};

@Injectable({
  providedIn: 'root'
})
export class WeatherService {
  private weatherDataSignal: WritableSignal<WeatherData> = signal({
    temperature: 100,
    isDay: 1,
    weatherCode: 0,
    windSpeed: 0
  });
  public weatherData = this.weatherDataSignal.asReadonly();

  private weatherIconSignal: WritableSignal<String> = signal(
    weather_types['sunny']
  );
  public weatherIcon = this.weatherIconSignal.asReadonly();

  constructor(protected http: HttpClient) {
    this.fetchWeatherData();
  }
  /**
   * Fetches weather data from open mateo using params defined above, and updates the weather signal.
   *
   * Gets the temperature, day/night distinction, weather code (cloudy/rainy/etc.), and wind speed for Sitterson Hall.
   */
  fetchWeatherData() {
    fetchWeatherApi(url, params).then((responses) => {
      const response = responses[0];
      const current = response.current()!;

      // Process the weather data
      this.weatherDataSignal.set({
        temperature: current.variables(0)!.value(),
        isDay: current.variables(1)!.value(),
        weatherCode: current.variables(2)!.value(),
        windSpeed: current.variables(3)!.value()
      });
      this.weatherIconSignal.set(this.assignWeatherIcon(this.weatherData()));
    });
  }
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

  private assignWeatherIcon(weatherData: WeatherData): string {
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
      (weatherData.weatherCode >= 50 && weatherData.weatherCode <= 69) ||
      (weatherData.weatherCode >= 80 && weatherData.weatherCode <= 84)
    ) {
      // Codes 50-69 indicate drizzle, rain, and freezing rain.
      // Codes 80-84 indicate different rain shower types (mixed w/ snow)
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
      if (weatherData.windSpeed >= 15) {
        return weather_types['partly_cloudy_windy'];
      } else {
        return weather_types['partly_cloudy'];
      }
    } else if (weatherData.windSpeed >= 15) {
      return weather_types['sunny_windy'];
    } else {
      // Default to sunny weather icon.
      return weather_types['sunny'];
    }
  }
}
