import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { JwtHelperService } from '@auth0/angular-jwt';
import { ReplaySubject, from, Observable, of } from 'rxjs';

const REPLAY_LAST = 1;

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  private isAuthenticated: ReplaySubject<boolean> = new ReplaySubject(REPLAY_LAST);
  public isAuthenticated$: Observable<boolean> = this.isAuthenticated.asObservable();

  constructor(private jwt: JwtHelperService, private router: Router) {
    this.authenticate();
  }

  public signOut(): void {
    localStorage.removeItem("bearerToken");
    this.router.navigate([""]);
    this.isAuthenticated.next(false);
  }

  private authenticate() {
    let token: string | Promise<string> | null = this.jwt.tokenGetter();
    if (token === null) {
      this.isAuthenticated.next(false);
    } else {
      let observable: Observable<string>;
      if (typeof token === 'string') {
        observable = of(token);
      } else {
        observable = from(token);
      }
      observable.subscribe((token) => {
        if (this.jwt.isTokenExpired(token)) {
          localStorage.removeItem('bearerToken');
          this.isAuthenticated.next(false);
        } else {
          this.isAuthenticated.next(true);
        }
      })
    }
  }

}
