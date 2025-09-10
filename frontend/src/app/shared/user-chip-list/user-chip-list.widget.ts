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
}
