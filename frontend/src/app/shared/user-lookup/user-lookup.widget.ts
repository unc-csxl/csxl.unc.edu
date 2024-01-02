/**
 * The User Lookup Widget allows users to search for users
 * in the XL.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import {
  Observable,
  ReplaySubject,
  debounceTime,
  filter,
  mergeMap,
  startWith
} from 'rxjs';
import { Profile } from 'src/app/models.module';
import { ProfileService, PublicProfile } from 'src/app/profile/profile.service';

@Component({
  selector: 'user-lookup',
  templateUrl: './user-lookup.widget.html',
  styleUrls: ['./user-lookup.widget.css']
})
export class UserLookup implements OnInit {
  @Input() profile!: Profile | null;
  @Input() users!: PublicProfile[];
  @Input() adminPermission!: boolean | null;

  userLookup = new FormControl();

  @ViewChild('usersInput') usersInput!: ElementRef<HTMLInputElement>;
  private filteredUsers: ReplaySubject<Profile[]> = new ReplaySubject();
  public filteredUsers$: Observable<Profile[]> =
    this.filteredUsers.asObservable();

  constructor(private profileService: ProfileService) {
    // Configure the filtered users list based on the form
    this.filteredUsers$ = this.userLookup.valueChanges.pipe(
      startWith(''),
      filter((search: string) => search.length > 2),
      debounceTime(100),
      mergeMap((search) => this.profileService.search(search))
    );
  }

  ngOnInit() {
    if (!this.adminPermission) {
      this.userLookup.disable();
    }
  }

  /** Handler for selecting an option in the who chip grid. */
  public onUserAdded(event: MatAutocompleteSelectedEvent) {
    let user = event.option.value as Profile;
    if (this.users.filter((e) => e.id === user.id).length == 0) {
      let organizer: PublicProfile = {
        id: user.id!,
        first_name: user.first_name!,
        last_name: user.last_name!,
        pronouns: user.pronouns!,
        email: user.email!,
        github_avatar: user.github_avatar
      };
      this.users.push(organizer);
    }

    this.usersInput.nativeElement.value = '';
    this.userLookup.setValue('');
  }

  /** Handler for selecting an option in the who chip grid. */
  public onUserRemoved(person: PublicProfile) {
    this.users.splice(this.users.indexOf(person), 1);
    this.userLookup.setValue('');
  }
}
