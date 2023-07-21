import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpResponse,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators'
import { NavigationService } from './navigation.service';

@Injectable({
    providedIn: 'root'
})
export class HttpRequestInterceptor implements HttpInterceptor {

  constructor(
    private navigationService: NavigationService
  ) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    if (request.method === "GET") {
      this.navigationService.setLoading(true);
    } else {
      this.navigationService.setSending(true);
    }

    return next.handle(request)
      .pipe(
        catchError((e) => {
            if (request.method === "GET") {
              this.navigationService.setLoading(false);
            } else {
              this.navigationService.setSending(false);
            }
            if (e instanceof HttpErrorResponse) {
                this.navigationService.error(e);
            }
            return of(e);
        }),
        tap((e) => {
            if (e instanceof HttpResponse) {
              if (request.method === "GET") {
                this.navigationService.setLoading(false);
              } else {
                this.navigationService.setSending(false);
              }
            }
        })
      );
  }
}