/**
 * The Organization Roster widget is responsible for displaying a club's roster for general users
 * as well as an interface for privileged users to accept/reject and edit memberships.
 *
 * @author Anika Ahmed, Alex Feng, Amy Xu, Alanna Zhang
 * @copyright 2025
 * @license MIT
 */

import { Component, Input, SimpleChanges } from '@angular/core';
import {
  Organization,
  OrganizationMembership,
  OrganizationJoinType,
  OrganizationMembershipStatus
} from '../../organization.model';
import { Profile } from 'src/app/models.module';
import { OrganizationRosterService } from '../../organization-roster.service';
import { PermissionService } from '../../../permission.service';
import { Observable, of } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { OrganizationRosterEditDialogComponent } from './organization-roster-widget-edit-dialog/organization-roster-widget-edit-dialog.component';

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
      this.checkPendingStatus(membership.status)
    );
  }

  /** Contents of the search bar */
  public searchBarQuery = '';

  /** Array of checked memberships for bulk deletion */
  protected selectedMemberships: OrganizationMembership[] = [];
  /** Deletes which are no longer visible but not yet finalized */
  protected stagedDeletes: OrganizationMembership[] = [];
  /** Updates which are locally applied but not yet committed */
  protected stagedUpdates: OrganizationMembership[] = [];
  /** Array of checked requests for bulk accept/reject */
  protected selectedRequests: OrganizationMembership[] = [];
  /** ID of the membership being edited for title/admin level */
  protected editingMembershipId: number | null = null;
  /** Original roster for reverting on cancel */
  originalRoster: OrganizationMembership[] = [];
  hasUnsavedChanges = false;

  constructor(
    private permissionService: PermissionService,
    private dialog: MatDialog
  ) {}

  inEditing() {
    return this.editing;
  }

  startEditing() {
    this.editing = true;
    this.originalRoster = JSON.parse(JSON.stringify(this.organizationRoster));
    return this.editing;
  }

  // ** Cancels editing and clears editing state. Also called after saving changes to clear state. */
  cancelEditing() {
    this.editing = false;
    this.selectedMemberships = [];
    // Restore dirty membership fields
    for (const changed of this.stagedUpdates) {
      changed.selected_title = undefined;
      changed.selected_permission_level = undefined;
    }
    // Restore deleted memberships if not already deleted
    for (const deleted of this.stagedDeletes) {
      const original = this.originalRoster.find((m) => m.id === deleted.id);
      if (
        original &&
        !this.organizationRoster.some((m) => m.id === original.id)
      ) {
        this.organizationRoster.push(original);
      }
    }
    this.stagedUpdates = [];
    this.stagedDeletes = [];
    this.hasUnsavedChanges = false;
    return this.editing;
  }

  confirmUpdate() {
    // Delete staged deletions
    this.removeMemberships(this.stagedDeletes);
    // Finalize dirty roster into official one
    this.originalRoster = this.organizationRoster;
    for (const membership of this.stagedUpdates) {
      if (
        membership.id &&
        membership.organization_slug &&
        (membership.selected_title !== undefined ||
          membership.selected_permission_level !== undefined)
      ) {
        this.organizationRosterService
          .updateOrganizationMembership(
            membership.organization_slug,
            membership.id,
            membership.user.id,
            membership.organization_id,
            membership.term.id,
            membership.selected_title ?? membership.title,
            membership.selected_permission_level ?? membership.permission_level
          )
          .subscribe((updatedMembership) => {
            const rosterItem = this.organizationRoster.find(
              (m) => m.id === membership.id
            );
            if (rosterItem) {
              // Finalizes value
              rosterItem.title = updatedMembership.title;
              rosterItem.permission_level = updatedMembership.permission_level;
            }
          });
      }
    }
    // Clear state
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

  openEditDialog(membership: OrganizationMembership) {
    // Initialize value to current selected values from session if any, otherwise use original values
    membership.selected_title = membership.selected_title ?? membership.title;
    membership.selected_permission_level =
      membership.selected_permission_level ?? membership.permission_level;

    const dialogRef = this.dialog.open(OrganizationRosterEditDialogComponent, {
      width: '500px',
      height: 'auto',
      maxHeight: '90vh',
      data: { ...membership }
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        membership.selected_title = result.selected_title;
        membership.selected_permission_level = result.selected_permission_level;
        if (!this.stagedUpdates.includes(membership)) {
          this.stagedUpdates.push(membership);
        }
        this.hasUnsavedChanges = this.hasActualChanges();
      }
    });
  }
  checkCount() {
    return this.selectedMemberships.length;
  }
  getTotalChangesCount() {
    // Staged deletes are always actual changes
    let changeCount = this.stagedDeletes.length;

    for (const membership of this.stagedUpdates) {
      const titleChanged = membership.selected_title !== membership.title;
      const permissionChanged =
        membership.selected_permission_level !== membership.permission_level;
      if (titleChanged || permissionChanged) {
        changeCount++;
      }
    }
    return changeCount;
  }
  private hasActualChanges(): boolean {
    return this.getTotalChangesCount() > 0;
  }
  checkPendingStatus(status: OrganizationMembershipStatus) {
    if (status === OrganizationMembershipStatus.PENDING) {
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
      membership.status === OrganizationMembershipStatus.PENDING
    )
      this.organizationRosterService
        .updateOrganizationMembership(
          membership.organization_slug,
          membership.id,
          membership.user.id,
          membership.organization_id,
          membership.term.id,
          membership.title,
          membership.permission_level,
          OrganizationMembershipStatus.ACTIVE
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
      membership.status === OrganizationMembershipStatus.PENDING
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
