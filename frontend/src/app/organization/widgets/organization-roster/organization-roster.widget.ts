import { Component, Input } from '@angular/core';
import { Organization, OrganizationMembership } from '../../organization.model';
import { Profile } from 'src/app/models.module';
import { OrganizationRosterService } from './organization-roster.widget.service';

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

  public searchBarQuery = '';
  constructor() {}
}
