/**
 * The Signage Service abstracts HTTP requests to the backend
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
  parseFastSignageDataJSON,
  parseSlowSignageDataJSON
} from './signage.model';

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

  constructor(protected http: HttpClient) {
    this.getSlowData();
    this.getFastData();
  }

  /**
   * Fetches the slow data from the backend, parses the JSON into the frontend model, and updates the signals
   *
   * @return SlowData Subscription
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
   * @return FastData Subscription
   */
  getFastData() {
    return this.http
      .get<FastSignageDataJSON>(`/api/signage/fast`)
      .pipe(map(parseFastSignageDataJSON))
      .subscribe((fastSignageData) => {
        this.fastDataSignal.set(fastSignageData);
      });
  }
}
