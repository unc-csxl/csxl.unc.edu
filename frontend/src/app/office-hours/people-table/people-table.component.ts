/**
 * The People Table Component displays all users in a given section
 * Instructors + TAs can elevate user roles
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import { OfficeHoursService } from '../office-hours.service';
import {
  SectionMember,
  SectionMemberPartial
} from 'src/app/academics/academics.models';
import { HttpErrorResponse } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

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

  constructor(
    private officeHoursService: OfficeHoursService,
    protected snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.getSectionMembers();
  }

  getSectionMembers() {
    this.officeHoursService
      .getSectionMembers(this.sectionId)
      .subscribe((section_members) => (this.sectionMembers = section_members));
  }

  formatRosterRole(typeNum: number) {
    return this.officeHoursService.formatRosterRole(typeNum);
  }

  // TODO: Need to add functionality to the selects
  onRoleChange(element: SectionMember) {
    // console.log(element);
    if (element.id == null) {
      console.log('error');
    } else {
      const member: SectionMemberPartial = {
        id: element.id,
        member_role: element.member_role
      };
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
