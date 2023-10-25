import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class NavigationService {
  private title: BehaviorSubject<string> = new BehaviorSubject('');
  public title$ = this.title.asObservable();

  private loading: BehaviorSubject<boolean> = new BehaviorSubject(false);
  public loading$ = this.loading.asObservable();

  private sending: BehaviorSubject<boolean> = new BehaviorSubject(false);
  public sending$ = this.sending.asObservable();

  private _error: BehaviorSubject<string | null> = new BehaviorSubject<
    string | null
  >(null);
  public error$ = this._error.asObservable();

  constructor() {}

  setTitle(title: string) {
    this._deferToNextChangeDetectionCycle(() => this.title.next(title));
  }

  setLoading(state: boolean) {
    this._deferToNextChangeDetectionCycle(() => this.loading.next(state));
  }

  setSending(state: boolean) {
    this._deferToNextChangeDetectionCycle(() => this.sending.next(state));
  }

  error(e: HttpErrorResponse) {
    this._deferToNextChangeDetectionCycle(() =>
      this._error.next(
        `Response: ${e.status} ${e.statusText}\nEndpoint: ${e.url}`
      )
    );
  }

  /**
   * For reasons that seem related to HttpRequestInterceptor's lifecycle of asynchronous operations
   * being outside the general lifecycle of change detection in angular components, the following
   * workaround method is used to defer updating navigation state until the next tick and, therefore,
   * next change detection cycle.
   *
   * Additional investigation may help determine a better means for achieving this, but for now
   * it avoids the previously commonly seen error of front-end state being changed outside CD cycle.
   *
   * @param operation the logic moved to next tick.
   */
  private _deferToNextChangeDetectionCycle(operation: () => void) {
    setTimeout(operation, 0);
  }
}
