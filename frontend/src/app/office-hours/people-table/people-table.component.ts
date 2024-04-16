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
import { SectionMember } from 'src/app/academics/academics.models';

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
  roles: string[] = ['Student', 'UTA', 'Instructor'];
  sectionMembers: SectionMember[] = [];

  constructor(private officeHoursService: OfficeHoursService) {}

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
    console.log(element);
  }

  formatEnum(role: string) {
    if (role === 'Student') {
      return 0;
    } else if (role === 'UTA') {
      return 1;
    } else return 3;
  }
}
