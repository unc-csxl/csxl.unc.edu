/**
 * The Reservation Editor allows students to both create and edit reservations.
 * 
 * @author Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { Component, ElementRef, ViewChild } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Profile } from 'src/app/models.module';
import { Observable, ReplaySubject, debounceTime, filter, mergeMap, startWith } from 'rxjs';
import { ProfileService } from 'src/app/profile/profile.service';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';

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

  public people: Profile[] = [];

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  // 'Who' Form Data
  public userLookup: FormControl = new FormControl();
  @ViewChild('whoInput') whoInput!: ElementRef<HTMLInputElement>;
  private filteredUsers: ReplaySubject<Profile[]> = new ReplaySubject();
  public filteredUsers$: Observable<Profile[]> = this.filteredUsers.asObservable();

  constructor(
    private route: ActivatedRoute,
    private profileService: ProfileService,
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar) {

    /** Get currently-logged-in user. */
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Add validators to the form */
    const form = this.reservationForm;
    // form.get('name')?.addValidators(Validators.required);

    /** Add current user as first value in the form */
    this.people.push(this.profile);

  }

  /** Actions to complete when the component loads. */
  public ngOnInit() {

    // Configure the filtered users list based on the form
    this.filteredUsers$ = this.userLookup.valueChanges.pipe(
      startWith(''),
      filter((search: string) => search.length > 2),
      debounceTime(100),
      mergeMap((search) => this.profileService.search(search))
    );
  }

  /** Handler for selecting an option in the who chip grid. */
  public onOptionSelected = (event: MatAutocompleteSelectedEvent) => {
    let user = event.option.value as Profile;
    if (this.people.filter(e => e.id === user.id).length == 0) {
      this.people.push(user);
    }
    this.whoInput.nativeElement.value = '';
    this.userLookup.setValue('');
  }

  /** Handler for selecting an option in the who chip grid. */
  public onOptionDeselected = (person: Profile) => {
    this.people.splice(this.people.indexOf(person), 1);
    this.userLookup.setValue('');
  }

  /** Formatter for the when tickmark thumbnail */
  formatLabel = (value: number): string => {
    let d = new Date(0);
    d.setUTCSeconds(value);

    return `${d.getHours() > 12 ? d.getHours() - 12 : d.getHours()}:${d.getMinutes() == 0 ? "00" : d.getMinutes()}${d.getHours() >= 12 ? "PM" : "AM"}`;
  }

  durationString = (start: number, end: number): string => {
    let minutes = (end - start) / 60
    if (minutes >= 60) {
      return `${Math.floor(minutes / 60)}hr ${minutes % 60}min`
    }
    return `${minutes % 60}min`
  }

}