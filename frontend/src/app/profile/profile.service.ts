import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, mergeMap, Observable, of, share, shareReplay, Subject, tap } from 'rxjs';
import { AuthenticationService } from '../authentication.service';

export interface Permission {
  id?: number;
  action: string;
  resource: string;
}

export interface Profile {
  id: number | null;
  pid: number;
  onyen: string;
  first_name: string | null;
  last_name: string | null;
  email: string | null;
  pronouns: string | null;
  github: string | null;
  github_id: number | null;
  github_avatar: string | null;
  registered: boolean;
  role: number;
  permissions: Permission[];
}

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  private profile: Subject<Profile | undefined> = new BehaviorSubject<Profile | undefined>(undefined);
  public profile$: Observable<Profile | undefined>;

  private isAuthenticated: boolean = false;

  constructor(protected http: HttpClient, protected auth: AuthenticationService) {
    this.profile$ = this.auth.isAuthenticated$.pipe(
      mergeMap(isAuthenticated => {
        this.isAuthenticated = isAuthenticated;
        if (isAuthenticated) {
          this.refreshProfile();
          return this.profile.asObservable()
        } else {
          return of(undefined);
        }
      })
    );
  }

  private refreshProfile() {
    if (this.isAuthenticated) {
      this.http.get<Profile>('/api/profile').subscribe(profile => this.profile.next(profile));
    }
  }

  put(profile: Profile) {
    return this.http.put<Profile>("/api/profile", profile).pipe(tap(profile => this.profile.next(profile)));
  }

  search(query: string) {
    let encodedQuery = encodeURIComponent(query);
    return this.http.get<Profile[]>(`/api/user?q=${encodedQuery}`);
  }

  getGitHubOAuthLoginURL(): Observable<string> {
    return this.http.get<string>("/oauth/github_oauth_login_url");
  }

  unlinkGitHub() {
    return this.http.delete("/oauth/github");
  }

}