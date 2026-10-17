import {
  HttpClient,
  HttpErrorResponse,
  HttpParams
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject, map, tap } from 'rxjs';
import {
  OperatingHours,
  OperatingHoursJSON,
  parseOperatingHoursJSON
} from './coworking.models';
import { TimeRangeJSON } from '../time-range';
import { CoworkingService } from './coworking.service';

/** Read and manage the facility's schedule through the operating-hours API. */
@Injectable({ providedIn: 'root' })
export class OperatingHoursService {
  private readonly url = '/api/coworking/operating_hours';
  private readonly changes = new Subject<void>();
  readonly changes$ = this.changes.asObservable();

  constructor(
    private http: HttpClient,
    private coworking: CoworkingService
  ) {}

  /** Includes intervals that overlap the requested window, including active hours. */
  list(start: string, end: Date): Observable<OperatingHours[]> {
    const params = new HttpParams()
      .set('start', start)
      .set('end', end.toISOString());
    return this.http
      .get<OperatingHoursJSON[]>(this.url, { params })
      .pipe(map((hours) => hours.map(parseOperatingHoursJSON)));
  }

  /** Form timestamps are facility-local, as accepted by the TimeRange API. */
  create(range: TimeRangeJSON): Observable<OperatingHours> {
    return this.http.post<OperatingHoursJSON>(this.url, range).pipe(
      map(parseOperatingHoursJSON),
      tap(() => this.refresh())
    );
  }

  /** Replace both times on the same persisted record. */
  update(id: number, range: TimeRangeJSON): Observable<OperatingHours> {
    return this.http.put<OperatingHoursJSON>(`${this.url}/${id}`, range).pipe(
      map(parseOperatingHoursJSON),
      tap(() => this.refresh())
    );
  }

  /** The server rechecks that the interval has not started. */
  delete(id: number): Observable<void> {
    return this.http
      .delete<void>(`${this.url}/${id}`)
      .pipe(tap(() => this.refresh()));
  }

  private refresh(): void {
    this.changes.next();
    this.coworking.pollStatus();
  }
}

export function operatingHoursError(error: HttpErrorResponse): string {
  if (error.status === 403)
    return 'You do not have permission to change these hours.';
  if (error.status === 404)
    return 'These hours are no longer available. Refresh the schedule.';
  if (error.status === 422)
    return 'Enter valid dates with the end time after the start time.';
  if (error.status === 409)
    return (
      error.error?.message ?? 'These hours conflict with the current schedule.'
    );
  return 'Unable to save the change. Please try again.';
}
