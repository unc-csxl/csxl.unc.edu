/**
 * The Profile About Card displays profile specific information
 * about a user, such as name, pfp, pronouns, and email.
 *
 * @author Jade Keegan
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { Profile } from '../../models.module';

@Component({
  selector: 'profile-about-card',
  templateUrl: './profile-about-card.widget.html',
  styleUrls: ['./profile-about-card.widget.css']
})
export class ProfileAboutCard {
  @Input() profile!: Profile;

  constructor() {}
}
