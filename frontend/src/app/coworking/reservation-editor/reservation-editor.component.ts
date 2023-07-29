/** Constructs the Reservation editor which allows users to create or edit reservations. */

import { Component } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Profile } from 'src/app/models.module';

@Component({
  selector: 'app-reservation-editor',
  templateUrl: './reservation-editor.component.html',
  styleUrls: ['./reservation-editor.component.css']
})
export class ReservationEditorComponent {

  public static Route: Route = {
    path: 'reservation/create',
    component: ReservationEditorComponent,
    title: 'Create Registration',
    resolve: { profile: profileResolver }
  };

  /** Create a form group */
  public reservationForm = this.formBuilder.group({

  });

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;


  constructor(
    private route: ActivatedRoute,
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar) {

    /** Get currently-logged-in user. */
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Add validators to the form */
    const form = this.reservationForm;
    // form.get('name')?.addValidators(Validators.required);

  }
}