/**
 * The TV Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Will Zahrt
 * @copyright 2024
 * @license MIT
 */

import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
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
export class SignageService {
  /** Constructor */
  constructor(protected http: HttpClient) {}

  getFastData(): Observable<FastSignageData> {
    return this.http
      .get<FastSignageDataJson>(`/api/signage/fast`)
      .pipe(map(parseFastSignageDataJson));
  }

  getSlowData(): Observable<SlowSignageData> {
    return this.http
      .get<SlowSignageDataJson>(`/api/signage/slow`)
      .pipe(map(parseSlowSignageDataJson));
  }
}
