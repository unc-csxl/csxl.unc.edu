/**
 * The Organization Details Info Card widget abstracts the implementation of each
 * individual organization detail card from the whole organization detail page.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney, Anika Ahmed, Alex Feng, Amy Xu, Alanna Zhang
 * @copyright 2025
 * @license MIT
 */

import { Component, Input, Output, EventEmitter } from '@angular/core';
import {
  Organization,
  OrganizationJoinType,
  OrganizationMembership,
  OrganizationMembershipStatus
} from '../../organization.model';
import { Profile } from '../../../profile/profile.service';
import { SocialMediaIconWidgetService } from 'src/app/shared/social-media-icon/social-media-icon.widget.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OrganizationRosterService } from '../../organization-roster.service';

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

  /** The snackbar from parent component, used to display join/leave status */
  @Input() snackBar: MatSnackBar | undefined;

  /** The user's membership, passed in from roster */
  @Input() membership?: OrganizationMembership;

  @Input() organizationRoster?: OrganizationMembership[] | undefined;

  @Input() organizationRosterService: OrganizationRosterService | undefined;

  /** Emits when the user joins or leaves the organization */
  @Output() membershipChanged = new EventEmitter<void>();

  /** Constructs the organization detail info card widget */
  constructor(private icons: SocialMediaIconWidgetService) {}

  isinOrganization() {
    if (
      this.profile &&
      this.profile.id != null &&
      this.organization != undefined
    ) {
      for (let organization of this.profile.organizations) {
        if (organization == this.organization.name) {
          return true;
        }
      }
    }
    return false;
  }

  checkActiveStatus(): boolean {
    return this.membership?.status === OrganizationMembershipStatus.ACTIVE;
  }

  checkPendingStatus(): boolean {
    return this.membership?.status === OrganizationMembershipStatus.PENDING;
  }

  getJoinButtonText(joinType: OrganizationJoinType | null): string {
    return joinType === 'Open'
      ? 'Join'
      : joinType === 'Apply'
        ? 'Apply'
        : 'Closed';
  }

  handleJoinOrganization(slug: string, profile_id: number) {
    this.organizationRosterService
      ?.addOrganizationMembership(slug, profile_id, this.organization?.id ?? 0)
      .subscribe({
        complete: () => {
          if (this.organization) {
            this.profile?.organizations.push(this.organization.name);
          }
          this.membershipChanged.emit();
        },
        error: () => {
          this.snackBar?.open('Unable to join organization', 'Close', {
            duration: 5000
          });
        }
      });
  }

  handleLeaveOrganization(slug: string) {
    if (this.membership) {
      this.organizationRosterService
        ?.deleteOrganizationMembership(slug, this.membership.id)
        .subscribe({
          complete: () => {
            if (this.organization) {
              const index = this.profile?.organizations.findIndex(
                (org) => org === this.organization?.name
              );
              if (index !== -1 && index != null) {
                this.profile?.organizations.splice(index, 1);
              }
            }
            this.membershipChanged.emit();
          },
          error: () => {
            this.snackBar?.open('Unable to leave organization', 'Close', {
              duration: 5000
            });
          }
        });
    }
  }

  /** Returns an ordered list of memberships to display as exec board */
  getExecBoardMembers(): OrganizationMembership[] {
    if (!this.organization || !this.organizationRoster) return [];
    // Filter out members with no special title
    const execs = this.organizationRoster.filter(
      (m) => m.title && m.title.trim().toLowerCase() !== 'member'
    );
    // Sort according to priority
    const priority = [
      'president',
      'co-president',
      'vice president',
      'treasurer',
      'secretary'
    ];
    return execs.sort((a, b) => {
      const aTitle = (a.title || '').toLowerCase();
      const bTitle = (b.title || '').toLowerCase();
      const aIndex = priority.findIndex((p) => aTitle.includes(p));
      const bIndex = priority.findIndex((p) => bTitle.includes(p));
      if (aIndex !== bIndex) {
        if (aIndex === -1) return 1;
        if (bIndex === -1) return -1;
        return aIndex - bIndex;
      }
      // If no priority specified, sort alphabetically
      return aTitle.localeCompare(bTitle);
    });
  }
}
