import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Profile, ProfileService } from '../profile/profile.service';

@Injectable({
  providedIn: 'root'
})
export class CheckInService {

  constructor(
    private http: HttpClient
  ) { }

  new_check_in(profile: Profile) : Observable<Profile> {
    return this.http.post<Profile>("/api/check-in", profile)
  }

}
