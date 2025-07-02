/**
 * This is the pipe used to filter organizations on the organizations page.
 *
 * @author Alex Feng
 * @copyright 2024
 * @license MIT
 */

import { Pipe, PipeTransform } from '@angular/core';
import { OrganizationMembership } from '../organization.model';

@Pipe({
  name: 'rosterFilter'
})
export class RosterFilterPipe implements PipeTransform {
  /** Returns a mapped array of organizations that start with the input string (if search query provided).
   * @param {Observable<OrganizationMembership[]>} roster: observable list of valid Organization models
   * @param {String} searchQuery: input string to filter by
   * @returns {Observable<OrganizationMembership[]>}
   */
  transform(
    roster: OrganizationMembership[],
    searchQuery: String
  ): OrganizationMembership[] {
    // Sort the organizations list alphabetically by name
    roster = roster.sort(
      (a: OrganizationMembership, b: OrganizationMembership) => {
        return (a.user.first_name + ' ' + a.user.last_name || '')
          .toLowerCase()
          .localeCompare(
            (b.user.first_name + ' ' + b.user.last_name || '').toLowerCase()
          );
      }
    );

    // If a search query is provided, return the organizations that start with the search query.
    if (searchQuery) {
      return roster.filter((roster) =>
        (roster.user.first_name + ' ' + roster.user.last_name || '')
          .toLowerCase()
          .includes(searchQuery.toLowerCase())
      );
    } else {
      // Otherwise, return the original list.
      return roster;
    }
  }
}
