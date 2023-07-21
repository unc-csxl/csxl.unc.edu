/** Creates a filter pipe for search bars used throughout the application. */

import { Pipe, PipeTransform } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { OrganizationSummary } from '../models.module';

@Pipe({
  name: 'filter'
})
export class FilterPipe implements PipeTransform {

  /** Returns a mapped array of organizations that start with the input string (if search query provided). 
   * @param {Observable<OrganizationSummary[]>} organizations: observable list of valid Organization models
   * @param {String} searchQuery: input string to filter by
   * @returns {Observable<OrganizationSummary[]>}
   */
  transform = (organizations: Observable<OrganizationSummary[]>, searchQuery: String) => {
    // Sort the organizations list alphabetically by name
    organizations = organizations.pipe(
      map(orgs => orgs.sort((a: OrganizationSummary, b: OrganizationSummary) => {
        if(a.name.toLowerCase() < b.name.toLowerCase()) {
          return -1;
        }
        else if(a.name.toLowerCase() > b.name.toLowerCase()) {
          return 1;
        }
        else {
          return 0;
        }
      }))
    )
    
    // If a search query is provided, return the organizations that start with the search query.
    if (searchQuery) {
      return organizations.pipe(
        map(organizations => organizations
          .filter(org => 
            org.name.toLowerCase().startsWith(searchQuery.toLowerCase()) ||
            org.short_description.toLowerCase().includes(searchQuery.toLowerCase()) ||
            org.long_description.toLowerCase().includes(searchQuery.toLowerCase()))));
    } else {
      // Otherwise, return the original list.
      return organizations;
    }
  }

}
