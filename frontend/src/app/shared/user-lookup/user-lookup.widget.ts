/**
 * The User Lookup Widget allows users to search for users
 * in the XL.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import {
  Component,
  ElementRef,
  EventEmitter,
  Input,
  OnInit,
  Output,
  ViewChild
} from '@angular/core';
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
  styleUrls: ['./user-lookup.widget.css'],
  standalone: false
})
export class UserLookup implements OnInit {
  @Input() label: string = 'Users';
  @Input() maxSelected: number | null = null;
  @Input() users: PublicProfile[] = [];
  @Input() initialUser?: PublicProfile;
  @Input() disabled: boolean | null = false;

  @Output() usersChanged: EventEmitter<PublicProfile[]> = new EventEmitter();

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
    if (this.disabled) {
      this.userLookup.disable();
    }
    if (this.initialUser) {
      this.users = [this.initialUser!];
    }
  }

  /** Handler for selecting an option in the who chip grid. */
  public onUserAdded(event: MatAutocompleteSelectedEvent) {
    let user = event.option.value as Profile;
    if (this.users.filter((e) => e.id === user.id).length == 0) {
      let organizer: PublicProfile = {
        id: user.id!,
        onyen: user.onyen,
        first_name: user.first_name!,
        last_name: user.last_name!,
        pronouns: user.pronouns!,
        email: user.email!,
        github_avatar: user.github_avatar,
        github: user.github,
        bio: user.bio,
        linkedin: user.linkedin,
        website: user.website,
        profile_emoji: user.profile_emoji,
        emoji_expiration: user.emoji_expiration
      };
      this.users.push(organizer);
    }
    this.usersInput.nativeElement.value = '';
    this.userLookup.setValue('');
    this.usersChanged.emit(this.users);
  }

  /** Handler for selecting an option in the who chip grid. */
  public onUserRemoved(person: PublicProfile) {
    this.users.splice(this.users.indexOf(person), 1);
    this.userLookup.setValue('');
    this.usersChanged.emit(this.users);
  }

  /** Check if emoji should be displayed for a user (not expired) */
  shouldDisplayEmoji(user: Profile | PublicProfile): boolean {
    if (!user.profile_emoji) return false;
    if (!user.emoji_expiration) return true;
    return new Date(user.emoji_expiration) > new Date();
  }

  /** Get display name with emoji if applicable */
  getDisplayName(user: Profile | PublicProfile): string {
    const name = `${user.first_name} ${user.last_name}`;
    if (this.shouldDisplayEmoji(user)) {
      return `${name} ${user.profile_emoji}`;
    }
    return name;
  }
}
