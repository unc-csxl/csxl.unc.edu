/**
 * The Organization Card widget abstracts the implementation of each
 * individual organization card from the whole organization page.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { Organization } from '../../organization.model';
import { Profile } from '../../../profile/profile.service';

@Component({
  selector: 'organization-card',
  templateUrl: './organization-card.widget.html',
  standalone: false
})
export class OrganizationCard {
  /** The organization to show */
  @Input() organization!: Organization;
  /** The profile of the currently signed in user */
  @Input() profile?: Profile;

  constructor() {}

  normalizedLogoUrl(logo: string): string {
    if (!logo) return logo;
    if (logo.includes('github.com') && logo.includes('/blob/')) {
      return logo
        .replace('https://github.com/', 'https://raw.githubusercontent.com/')
        .replace('/blob/', '/');
    }
    if (logo.startsWith('http://')) {
      return logo.replace('http://', 'https://');
    }
    return logo;
  }
}
