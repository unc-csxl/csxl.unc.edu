/**
 * The People Table Component displays all users in a given section
 * Instructors + TAs can elevate user roles
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import { OfficeHoursService } from '../../office-hours.service';
import {
  RosterRole,
  SectionMember,
  SectionMemberPartial
} from 'src/app/academics/academics.models';
import { HttpErrorResponse } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AcademicsService } from 'src/app/academics/academics.service';

@Component({
  selector: 'people-table',
  templateUrl: './people-table.component.html',
  styleUrls: ['./people-table.component.css']
})
export class PeopleTableComponent implements OnInit {
  @Input() sectionId!: number;
  public displayedPeopleColumns: string[] = [
    'first-name',
    'last-name',
    'pronouns',
    'role'
  ];
  roles: string[] = ['Student', 'UTA', 'GTA', 'Instructor'];
  sectionMembers: SectionMember[] = [];
  rosterRole: RosterRole | null;

  constructor(
    private officeHoursService: OfficeHoursService,
    private academicsService: AcademicsService,
    protected snackBar: MatSnackBar
  ) {
    this.rosterRole = null;
  }

  ngOnInit(): void {
    this.initializeData();
  }

  initializeData(): void {
    this.checkRosterRole().then(() => {
      // RosterRole is retrieved, so good to go on other actions
      this.getSectionMembers();
    });
  }

  // Check RosterRole of subject so that correct table can be displayed
  checkRosterRole(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.academicsService.getMembershipBySection(this.sectionId).subscribe(
        (section_member) => {
          this.rosterRole = section_member.member_role;
          resolve(); // Resolve the Promise when the roster role is set
        },
        (error) => {
          reject(error); // Reject the Promise if there's an error
        }
      );
    });
  }

  getSectionMembers() {
    this.officeHoursService
      .getSectionMembers(this.sectionId)
      .subscribe((section_members) => (this.sectionMembers = section_members));
  }

  formatRosterRole(typeNum: number) {
    return this.officeHoursService.formatRosterRole(typeNum);
  }

  onRoleChange(element: SectionMember, role: number) {
    // SectionMember model allows for null ids, so need to add this check
    if (element.id == null) {
      this.onError(
        new HttpErrorResponse({
          error: 'SectionMember not found',
          status: 404
        })
      );
    } else {
      // Build a partial with the Member's id and the target new role
      const member: SectionMemberPartial = {
        id: element.id,
        member_role: role
      };
      // Pass partial into updateMemberRole service method
      this.officeHoursService
        .updateMemberRole(member, this.sectionId)
        .subscribe({
          next: () => this.onSuccess(),
          error: (err) => this.onError(err)
        });
    }
  }

  formatEnum(role: string) {
    if (role === 'Student') {
      return 0;
    } else if (role === 'UTA') {
      return 1;
    } else if (role === 'GTA') {
      return 2;
    } else return 3;
  }

  private onError(err: HttpErrorResponse): void {
    this.snackBar.open('Error occurred when trying to update member role', '', {
      duration: 5000
    });
  }

  private onSuccess(): void {
    this.snackBar.open('Member role has been updated!', '', {
      duration: 4000
    });
  }
}
