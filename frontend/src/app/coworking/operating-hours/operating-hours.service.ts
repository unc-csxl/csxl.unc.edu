import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { OperatingHours } from '../coworking.models';
import { Observable } from 'rxjs';
import { TimeRange } from 'src/app/time-range';

@Injectable({
  providedIn: 'root'
})
export class OperatingHoursService {
  protected http = inject(HttpClient);

  getOperatingHours(): Observable<OperatingHours[]> {
    const start = new Date();
    const end = new Date();
    end.setFullYear(end.getFullYear() + 1); // 1 year in the future

    const params = {
      start: start.toISOString(),
      end: end.toISOString()
    };

    return this.http.get<OperatingHours[]>('/api/coworking/operating_hours', {
      params
    });
  }

  newOperatingHours(timeRange: TimeRange) {
    return this.http.post(`/api/coworking/operating_hours`, timeRange);
  }

  deleteOperatingHours(id: number) {
    return this.http.delete(`/api/coworking/operating_hours/${id}`);
  }
}
