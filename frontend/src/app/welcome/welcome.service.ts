/**
 * The Welcome Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha
 * @copyright 2024 <agandecha@unc.edu>
 * @license MIT
 */

import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {
  WelcomeOverview,
  WelcomeOverviewJson,
  parseWelcomeOverviewJson
} from './welcome.model';
import { Observable, map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WelcomeService {
  /** Constructor */
  constructor(protected http: HttpClient) {}

  /**
   * Retrieves the current welcome page status from the API.
   * @returns { Observable<WelcomeOverview> }
   */
  getWelcomeStatus(): Observable<WelcomeOverview> {
    return this.http
      .get<WelcomeOverviewJson>(`/api/articles/welcome`)
      .pipe(map(parseWelcomeOverviewJson));
  }

  /**
   * Retrieves the current welcome page status from the API
   * if the user is not logged in.
   * @returns { Observable<WelcomeOverview> }
   */
  getWelcomeStatusUnauthenticated(): Observable<WelcomeOverview> {
    return this.http
      .get<WelcomeOverviewJson>(`/api/articles/welcome/unauthenticated`)
      .pipe(map(parseWelcomeOverviewJson));
  }
}
