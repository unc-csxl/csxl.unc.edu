import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, ReplaySubject, Subject, tap } from 'rxjs';
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
  has_agreed: boolean;
}

export interface PublicProfile {
  id: number;
  first_name: string;
  last_name: string;
  pronouns: string;
  email: string;
  github_avatar: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class ProfileService {
  private profile: Subject<Profile | undefined> = new ReplaySubject(1);
  public profile$: Observable<Profile | undefined> =
    this.profile.asObservable();

  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService
  ) {
    this.auth.isAuthenticated$.subscribe((isAuthenticated) =>
      this.refreshProfile(isAuthenticated)
    );
  }

  private refreshProfile(isAuthenticated: boolean) {
    if (isAuthenticated) {
      this.http.get<Profile>('/api/profile').subscribe({
        next: (profile) => this.profile.next(profile),
        error: () => this.profile.next(undefined)
      });
    } else {
      this.profile.next(undefined);
    }
  }

  put(profile: Profile) {
    return this.http
      .put<Profile>('/api/profile', profile)
      .pipe(tap((profile) => this.profile.next(profile)));
  }

  search(query: string) {
    let encodedQuery = encodeURIComponent(query);
    return this.http.get<Profile[]>(`/api/user?q=${encodedQuery}`);
  }

  getGitHubOAuthLoginURL(): Observable<string> {
    return this.http.get<string>('/oauth/github_oauth_login_url');
  }

  unlinkGitHub() {
    return this.http.delete('/oauth/github');
  }
}
