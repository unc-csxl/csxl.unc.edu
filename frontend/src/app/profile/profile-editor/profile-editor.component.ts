import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from '../profile.resolver';
import { Profile, ProfileService } from '../profile.service';
import { CommunityAgreement } from 'src/app/shared/community-agreement/community-agreement.widget';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  standalone: false
})
export class ProfileEditorComponent implements OnInit {
  public static Route: Route = {
    path: 'edit',
    component: ProfileEditorComponent,
    title: 'Profile',
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  public profile: Profile;
  public token: string;
  public showToken: boolean = false;

  public profileForm = this.formBuilder.group({
    first_name: '',
    last_name: '',
    email: '',
    website: '',
    linkedin: '',
    pronouns: '',
    bio: ''
  });

  constructor(
    route: ActivatedRoute,
    protected formBuilder: FormBuilder,
    protected profileService: ProfileService,
    protected snackBar: MatSnackBar,
    protected dialog: MatDialog,
    private router: Router
  ) {
    const form = this.profileForm;
    form.get('first_name')?.addValidators(Validators.required);
    form.get('lastname')?.addValidators(Validators.required);
    form
      .get('email')
      ?.addValidators([
        Validators.required,
        Validators.email,
        Validators.pattern(/unc\.edu$/)
      ]);
    form.get('pronouns')?.addValidators(Validators.required);

    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    this.token = `${localStorage.getItem('bearerToken')}`;
  }

  ngOnInit(): void {
    let profile = this.profile;

    this.profileForm.setValue({
      first_name: profile.first_name,
      last_name: profile.last_name,
      email: profile.email,
      pronouns: profile.pronouns,
      bio: profile.bio,
      linkedin: profile.linkedin,
      website: profile.website
    });
  }

  onSubmit(): void {
    if (this.profileForm.valid) {
      Object.assign(this.profile, this.profileForm.value);
      if (!this.profile.accepted_community_agreement) {
        const dialogRef = this.dialog.open(CommunityAgreement, {
          disableClose: true,
          autoFocus: 'dialog'
        });
        dialogRef.afterClosed().subscribe((profile) => {
          this.profile.accepted_community_agreement = true;
        });
      }
      this.profileService.put(this.profile).subscribe({
        next: (user) => this.onSuccess(user),
        error: (err) => this.onError(err)
      });
    }
  }

  private onSuccess(profile: Profile) {
    this.router.navigate(['/profile']);
    this.snackBar.open('Profile Saved', '', { duration: 2000 });
  }

  private onError(err: any) {
    console.error('How to handle this?');
  }
}
