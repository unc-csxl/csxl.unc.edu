/**
 * This is the pipe used to filter organizations on the organizations page.
 *
 * @author Jade Keegan
 * @copyright 2023
 * @license MIT
 */

import { Pipe, PipeTransform } from '@angular/core';
import { Organization } from '../organization.model';

@Pipe({
  name: 'organizationFilter'
})
export class OrganizationFilterPipe implements PipeTransform {
  /** Returns a mapped array of organizations that start with the input string (if search query provided).
   * @param {Observable<Organization[]>} organizations: observable list of valid Organization models
   * @param {String} searchQuery: input string to filter by
   * @returns {Observable<Organization[]>}
   */
  transform(
    organizations: Organization[],
    searchQuery: String
  ): Organization[] {
    // Sort the organizations list alphabetically by name
    organizations = organizations.sort((a: Organization, b: Organization) => {
      return a.name.toLowerCase().localeCompare(b.name.toLowerCase());
    });

    // If a search query is provided, return the organizations that start with the search query.
    if (searchQuery) {
      return organizations.filter(
        (organization) =>
          organization.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          organization.short_description
            .toLowerCase()
            .includes(searchQuery.toLowerCase()) ||
          organization.long_description
            .toLowerCase()
            .includes(searchQuery.toLowerCase())
      );
    } else {
      // Otherwise, return the original list.
      return organizations;
    }
  }
}
