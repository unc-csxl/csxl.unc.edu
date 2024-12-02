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

  ngOnInit(): void {
    this.getSlowData();
    this.getFastData();
  }
}
