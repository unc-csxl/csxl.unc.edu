import { Component, Input } from '@angular/core';
import {
  Organization,
  OrganizationMembership,
  OrganizationRole
} from '../../organization.model';
import { Profile } from 'src/app/models.module';
import { OrganizationRosterService } from './organization-roster.widget.service';
import { PermissionService } from '../../../permission.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'organization-roster',
  templateUrl: './organization-roster.widget.html',
  styleUrls: ['./organization-roster.widget.css']
})
export class OrganizationRoster {
  // Organization to perform operations on
  @Input() organization!: Organization | undefined;
  // Service to perform operations with
  @Input() organizationRosterService!: OrganizationRosterService;
  // Roster that has been pre-fetched
  @Input() organizationRoster!: OrganizationMembership[];
  // User if they are logged in
  @Input() profile?: Profile;
  // Displays in organization-editing interface
  public editing?: boolean;

  /** Resposible for showing editable roster view in HTML code when admin signed in.
   * @returns {Observable<boolean>}
   */
  adminPermissions(): Observable<boolean> {
    return this.permissionService.check('organization.create', '*');
  }

  /** Store the content of the search bar */
  public searchBarQuery = '';

  protected selectedMemberships: OrganizationMembership[] = [];
  protected stagedDeletes: OrganizationMembership[] = [];
  originalRoster: OrganizationMembership[] = [];

  roles: OrganizationRole[] = [
    OrganizationRole.PRESIDENT,
    OrganizationRole.OFFICER,
    OrganizationRole.MEMBER,
    OrganizationRole.ADMIN,
    OrganizationRole.PENDING
  ];

  constructor(private permissionService: PermissionService) {}

  selectRole(role: OrganizationRole, membership: OrganizationMembership): void {
    membership.selected_role = role;
  }

  inEditing() {
    return this.editing;
  }

  startEditing() {
    this.editing = true;
    this.originalRoster = JSON.parse(JSON.stringify(this.organizationRoster));
    return this.editing;
  }

  cancelEditing() {
    this.editing = false;
    this.selectedMemberships = [];
    this.organizationRoster = this.originalRoster;
    return this.editing;
  }

  confirmUpdate() {
    this.removeMemberships(this.stagedDeletes);
    this.selectedMemberships = [];
    for (const membership of this.organizationRoster) {
      if (membership.id && membership.organization_slug)
        this.organizationRosterService
          .updateOrganizationMembership(
            membership.organization_slug,
            membership.id,
            membership.selected_role
              ? membership.selected_role
              : membership.organization_role
          )
          .subscribe((updatedMembership) => {
            const rosterItem = this.organizationRoster.find(
              (m) => m.id === membership.id
            );
            if (rosterItem) {
              rosterItem.organization_role =
                updatedMembership.organization_role;
            }
            this.originalRoster = this.organizationRoster;
            this.cancelEditing();
          });
    }
  }

  protected toggleSelectedMembership(
    membership: OrganizationMembership,
    selected: boolean
  ) {
    if (selected) {
      this.selectedMemberships.push(membership);
    } else {
      this.selectedMemberships.splice(
        this.selectedMemberships.indexOf(membership),
        1
      );
    }
  }

  checkCount() {
    return this.selectedMemberships.length;
  }
  checkPending(role: any) {
    console.log({ role });
    if (role === 'Membership pending') {
      return true;
    }
    return false;
  }

  protected removeMemberships(memberships: OrganizationMembership[]) {
    for (const membership of memberships) {
      if (membership.id && membership.organization_slug) {
        this.organizationRosterService
          .deleteOrganizationMembership(
            membership.organization_slug,
            membership.id
          )
          .subscribe();
      }
    }
    this.selectedMemberships = [];
  }

  protected acceptRequest = (membership: OrganizationMembership) => {
    if (membership.id !== null)
      this.organizationRosterService
        .updateOrganizationMembership(
          membership.organization_slug,
          membership.id,
          OrganizationRole.MEMBER
        )
        .subscribe(() => {
          this.organizationRoster = this.organizationRoster.filter(
            (m) => m.id !== membership.id
          );
        });
  };

  protected rejectRequest = (membership: OrganizationMembership) => {
    if (membership.id !== null)
      this.organizationRosterService
        .deleteOrganizationMembership(
          membership.organization_slug,
          membership.id
        )
        .subscribe(() => {
          this.organizationRoster = this.organizationRoster.filter(
            (m) => m.id !== membership.id
          );
        });
  };

  protected stageDeletes = (memberships: OrganizationMembership[]) => {
    this.stagedDeletes = memberships;
    for (const membership of memberships) {
      this.organizationRoster = this.organizationRoster.filter(
        (member) => member.id !== membership.id
      );
    }
    this.selectedMemberships = [];
  };
}
