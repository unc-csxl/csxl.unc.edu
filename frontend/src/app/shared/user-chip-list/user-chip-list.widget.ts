/**
 * The User Chip List Widget displays user names as MatChips with
 * an optional "click to contact" feature.
 *
 * @author Jade Keegan
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { PublicProfile } from 'src/app/profile/profile.service';

@Component({
    selector: 'user-chip-list',
    templateUrl: './user-chip-list.widget.html',
    styleUrls: ['./user-chip-list.widget.css'],
    standalone: false
})
export class UserChipList {
  @Input() users!: PublicProfile[];
  @Input() nameSuffix?: string = '';
  @Input() enableMailTo!: boolean;
  @Input() clickable?: boolean = true;
  constructor() {}

  emailRedirect(user: PublicProfile) {
    window.location.href = `mailto:${user.email}`;
  }

  /** Check if emoji should be displayed for a user (not expired) */
  shouldDisplayEmoji(user: PublicProfile): boolean {
    if (!user.profile_emoji) return false;
    if (!user.emoji_expiration) return true;
    return new Date(user.emoji_expiration) > new Date();
  }

  /** Get display name with emoji if applicable */
  getDisplayName(user: PublicProfile): string {
    const name = `${user.first_name} ${user.last_name}${this.nameSuffix}`;
    if (this.shouldDisplayEmoji(user)) {
      return `${name} ${user.profile_emoji}`;
    }
    return name;
  }
}
