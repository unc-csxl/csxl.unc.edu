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
    private htpClient: HttpClient
  ) { }

  new_check_in(profile: Profile) : Observable<Profile> {


    return this.htpClient.post<Profile>("/api/check-in", profile)


  }

}
