import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class NavigationService {

  private title: BehaviorSubject<string> = new BehaviorSubject("");
  public title$ = this.title.asObservable();

  private loading: BehaviorSubject<boolean> = new BehaviorSubject(false);
  public loading$ = this.loading.asObservable();

  private sending: BehaviorSubject<boolean> = new BehaviorSubject(false);
  public sending$ = this.sending.asObservable();

  private _error: BehaviorSubject<string | null> = new BehaviorSubject<string | null>(null);
  public error$ = this._error.asObservable();

  constructor() {}

  setTitle(title: string) {
    this.title.next(title);
  }

  setLoading(state: boolean) {
    this.loading.next(state);
  }

  setSending(state: boolean) {
    this.sending.next(state);
  }

  error(e: HttpErrorResponse) {
    this._error.next(`Response: ${e.status} ${e.statusText}\nEndpoint: ${e.url}`);
  }

}