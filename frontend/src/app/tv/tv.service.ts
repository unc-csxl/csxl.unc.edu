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
  FastTvData,
  FastTvDataJson,
  SlowTvData,
  SlowTvDataJson,
  parseFastTvDataJson,
  parseSlowTvDataJson
} from './tv.model';

@Injectable({
  providedIn: 'root'
})
export class TvService {
  /** Constructor */
  constructor(protected http: HttpClient) {}

  getFastData(): Observable<FastTvData> {
    return this.http
      .get<FastTvDataJson>(`/api/signage/fast`)
      .pipe(map(parseFastTvDataJson));
  }

  getSlowData(): Observable<SlowTvData> {
    return this.http
      .get<SlowTvDataJson>(`/api/signage/slow`)
      .pipe(map(parseSlowTvDataJson));
  }
}
