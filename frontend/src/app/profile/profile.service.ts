import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { mergeMap, Observable, of, shareReplay } from 'rxjs';
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

  public profile$!: Observable<Profile | undefined>;

  constructor(protected http: HttpClient, protected auth: AuthenticationService) {
    this.refreshProfile();
  }

  private refreshProfile() {
    this.profile$ = this.auth.isAuthenticated$.pipe(
      mergeMap(isAuthenticated => {
        if (isAuthenticated) {
          return this.http.get<Profile>('/api/profile');
        } else {
          return of(undefined);
        }
      }),
      shareReplay(1)
    );
  }

  put(profile: Profile) {
    return this.http.put<Profile>("/api/profile", profile);
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