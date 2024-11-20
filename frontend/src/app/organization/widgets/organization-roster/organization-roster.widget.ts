import { Component, Input } from '@angular/core';
import { OrganizationMembership } from '../../organization.model';

@Component({
  selector: 'organization-roster',
  templateUrl: './organization-roster.widget.html',
  styleUrls: ['./organization-roster.widget.css']
})
export class OrganizationRoster {
  /** The organization to show */
  @Input() organizationRoster!: OrganizationMembership[] | undefined;

  public searchBarQuery = '';
  constructor() {}
}
