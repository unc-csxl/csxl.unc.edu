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
import { AuthenticationService } from '../authentication.service';

@Injectable({
    providedIn: 'root'
})
export class HttpRequestInterceptor implements HttpInterceptor {

  constructor(
    private navigationService: NavigationService,
    private authService: AuthenticationService
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
              if (e.status === 401) {
                this.authService.signOut();
              } else {
                this.navigationService.error(e);
              }
              throw e;
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