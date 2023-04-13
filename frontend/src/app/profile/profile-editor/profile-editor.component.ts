import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from '../profile.resolver';
import { ProfileService } from '../profile.service';
import { Profile } from 'src/app/models.module';

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css']
})
export class ProfileEditorComponent implements OnInit {

  public static Route: Route = {
    path: 'profile-editor',
    component: ProfileEditorComponent, 
    title: 'Profile Editor', 
    canActivate: [isAuthenticated], 
    resolve: { profile: profileResolver }
  };

  public profile: Profile;

  public profileForm = this.formBuilder.group({
    first_name: '',
    last_name: '',
    email: '',
    pronouns: ''
  });

  constructor(route: ActivatedRoute, private router: Router, protected formBuilder: FormBuilder, protected profileService: ProfileService, protected snackBar: MatSnackBar) {
    const form = this.profileForm;
    form.get('first_name')?.addValidators(Validators.required);
    form.get('lastname')?.addValidators(Validators.required);
    form.get('email')?.addValidators([Validators.required, Validators.email, Validators.pattern(/unc\.edu$/)]);
    form.get('pronouns')?.addValidators(Validators.required);

    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;
  }

  ngOnInit(): void {
    let profile = this.profile;

    this.profileForm.setValue({
      first_name: profile.first_name,
      last_name: profile.last_name,
      email: profile.email,
      pronouns: profile.pronouns
    });
  }

  onSubmit(): void {
    if (this.profileForm.valid) {
      Object.assign(this.profile, this.profileForm.value)
      this.profileService.put(this.profile).subscribe(
        {
          next: (user) => this.onSuccess(user),
          error: (err) => this.onError(err)
        } 
      );
      this.router.navigate(['/profile']);
    }
  }

  private onSuccess(profile: Profile) {
    this.snackBar.open("Profile Saved", "", { duration: 2000 })
  }

  private onError(err: any) {
    console.error("How to handle this?");
  }

}