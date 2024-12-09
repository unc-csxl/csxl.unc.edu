/**
 * The Organization Details Info Card widget abstracts the implementation of each
 * individual organization detail card from the whole organization detail page.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { Organization } from '../../organization.model';
import { Profile } from '../../../profile/profile.service';
import { SocialMediaIconWidgetService } from 'src/app/shared/social-media-icon/social-media-icon.widget.service';

@Component({
  selector: 'organization-details-info-card',
  templateUrl: './organization-details-info-card.widget.html',
  styleUrls: ['./organization-details-info-card.widget.css']
})
export class OrganizationDetailsInfoCard {
  /** The organization to show */
  @Input() organization: Organization | undefined;
  /** The currently logged in user */
  @Input() profile?: Profile;
  /** Whether or not the user has permission to create events */
  @Input() eventCreationPermissions!: boolean | null;
  /** The parent's join org method */
  @Input() joinOrganizationMethod!: (slug: string, user_id: number) => void;

  /** Constructs the organization detail info card widget */
  constructor(private icons: SocialMediaIconWidgetService) {}
}
