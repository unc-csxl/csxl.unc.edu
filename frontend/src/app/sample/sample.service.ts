/** Sample service to show off OpenAPI integration */
import { inject, Injectable } from '@angular/core';
import { OpenApiHHTPClient } from './openapi-http-client';
import { components } from '../schema';

@Injectable({
  providedIn: 'root'
})
export class SampleService {
  // Inject new, type-safe HTTPClient abstraction
  private http = inject(OpenApiHHTPClient);
  sampleService: any;

  // This special example method wraps TanStack Query, providing back
  // a reactive (signal-based) object with loading states and caching.
  // See: https://tanstack.com/query/v5/docs/framework/angular/overview
  queryGetAll() {
    return this.http.queryGet('/api/sample');
  }

  getAll() {
    return this.http.get('/api/sample');
  }

  get(id: number) {
    return this.http.get('/api/sample/{id}', {
      pathParams: {
        id: id
      }
    });
  }

  create(request: components['schemas']['CreateSampleItemRequest']) {
    return this.http.post('/api/sample', {
      body: request
    });
  }
}
