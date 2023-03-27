import { Component } from '@angular/core';
import { Observable, map } from 'rxjs';
import { AuthenticationService } from '../authentication.service';
import { Profile, ProfileService } from '../profile/profile.service';
import { CheckInService } from './check-in.service';

@Component({
  selector: 'app-check-in',
  templateUrl: './check-in.component.html',
  styleUrls: ['./check-in.component.css']
})
export class CheckInComponent {
  public static Route = {
    path: 'check-in',
    component: CheckInComponent 
  }

  public isAuthenticated : Observable<boolean>;

  constructor(
    private authService: AuthenticationService,
    private checkInService: CheckInService,
    private profileService: ProfileService
  )  {
    this.isAuthenticated = authService.isAuthenticated$;
  }

  public userClicked() : void {
    this.profileService.profile$.subscribe({
      next: (data) => {
        if (data !== undefined) {
          this.checkInService.new_check_in(data).subscribe({
            next: (result) => this.onSuccess(result),
            error: (err) => this.onError(err)
          })
        }
      }
    })
  }

  public onSuccess(profile: Profile) : void {
    window.alert(`Thanks for checking, ${profile.first_name} ${profile.last_name}`!)
  }

  public onError(error: Error) : void {
    if (error.message) {
      window.alert(`There was an error checking you in: ${error.message}`)
    }
    else {
      window.alert("There was an unknown error when checking you in!")
    }
  }

}
