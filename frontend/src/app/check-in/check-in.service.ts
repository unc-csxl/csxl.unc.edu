import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Profile } from '../profile/profile.service';

export interface CheckIn {
  profile: Profile;
  time: Date;
}


@Injectable({
  providedIn: 'root'
})
export class CheckInService {

  constructor(
    private http: HttpClient
  ) { }

  private connect_to_backend : boolean = false;

  new_check_in(profile: Profile) : Observable<Profile> {

    if (this.connect_to_backend) {
      return this.http.post<Profile>("/api/check-in", profile)
    }
    else {
      return of(profile)
    }


  }

}
