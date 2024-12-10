
import { Component, Input, SimpleChanges } from '@angular/core';
import {
  Organization,
  OrganizationMembership,
  OrganizationRole,
  OrganizationJoinType
} from '../../organization.model';
import { Profile } from 'src/app/models.module';
import { OrganizationRosterService } from './organization-roster.widget.service';
import { PermissionService } from '../../../permission.service';
import { Observable, of } from 'rxjs';

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
  adminPermissions(slug: String | undefined): Observable<boolean> {
    if (slug) {
      return this.permissionService.check(
        'organization.update',
        `organization/${slug}`
      );
    }
    return of(false);
  }

  // Responsible for auto-updating the roster when join type changes
  ngOnChanges(changes: SimpleChanges) {
    if (changes['organization'] && changes['organization'].currentValue) {
      const previousJoinType = changes['organization'].previousValue?.join_type;
      const currentJoinType = changes['organization'].currentValue.join_type;

      if (previousJoinType !== currentJoinType) {
        console.log('Join type changed:', {
          previousJoinType,
          currentJoinType
        });
        this.handleJoinTypeChange(currentJoinType);
      }
      this.organization = changes['organization'].currentValue;
    }
  }

  private handleJoinTypeChange(newJoinType: OrganizationJoinType | null) {
    switch (newJoinType) {
      case 'Open':
        this.acceptRequests(this.getPendingRequests());
        break;
      case 'Closed':
        this.rejectRequests(this.getPendingRequests());
        break;
      case 'Apply':
        break;
    }
  }

  private getPendingRequests(): OrganizationMembership[] {
    return this.organizationRoster.filter((membership) =>
      this.checkPending(membership.organization_role)
    );
  }

  /** Store the content of the search bar */
  public searchBarQuery = '';

  protected selectedMemberships: OrganizationMembership[] = [];
  protected stagedDeletes: OrganizationMembership[] = [];
  protected selectedRequests: OrganizationMembership[] = [];
  originalRoster: OrganizationMembership[] = [];
  hasUnsavedChanges = false;

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
    this.hasUnsavedChanges = true;
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
    this.originalRoster = this.organizationRoster;
    this.selectedMemberships = [];
    for (const membership of this.organizationRoster) {
      if (
        membership.id &&
        membership.organization_slug &&
        membership.selected_role
      )
        this.organizationRosterService
          .updateOrganizationMembership(
            membership.organization_slug,
            membership.id,
            membership.selected_role
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
          });
    }
    this.hasUnsavedChanges = false;
    this.cancelEditing();
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
    if (
      membership.id !== null &&
      membership.organization_role === OrganizationRole.PENDING
    )
      this.organizationRosterService
        .updateOrganizationMembership(
          membership.organization_slug,
          membership.id,
          OrganizationRole.MEMBER
        )
        .subscribe((updatedMembership) => {
          this.organizationRoster = this.organizationRoster.filter(
            (m) => m.id !== membership.id
          );
          this.organizationRoster.push(updatedMembership);
        });
  };

  protected rejectRequest = (membership: OrganizationMembership) => {
    if (
      membership.id !== null &&
      membership.organization_role === OrganizationRole.PENDING
    )
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
    this.hasUnsavedChanges = true;
  };

  // Configurable for a selection of requests
  // Currently used to select all requests for the purpose of opening/closing a club
  protected acceptRequests = (memberships: OrganizationMembership[]) => {
    for (const membership of memberships) {
      this.acceptRequest(membership);
    }
  };

  protected rejectRequests = (memberships: OrganizationMembership[]) => {
    for (const membership of memberships) {
      this.rejectRequest(membership);
    }
  };
}
