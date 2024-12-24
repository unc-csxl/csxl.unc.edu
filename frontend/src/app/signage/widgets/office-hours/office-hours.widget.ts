/**
 * Office Hours Widget to Display all currently active office hours, their locations, and queue length
 *
 * @author Andrew Lockard <andrew.lockard15@gmail.com>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { SignageOfficeHours } from '../../signage.model';

type LocationHoursMap = { [location: string]: SignageOfficeHours[] };

// Used to calculate which Locations will be stored on each column
interface Column {
  locations: string[];
  totalHours: number;
}

@Component({
  selector: 'office-hours-display',
  templateUrl: './office-hours.widget.html',
  styleUrl: './office-hours.widget.css'
})
export class OfficeHoursWidget implements OnChanges {
  @Input() officeHours!: SignageOfficeHours[];
  sortedHours: LocationHoursMap = {};
  columns: Column[] = [];

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['officeHours']) {
      this.sortedHours = this.officeHours.reduce((acc, curr) => {
        if (!acc[curr.location]) {
          acc[curr.location] = [];
        }

        // Add the current to it's location list
        acc[curr.location].push(curr);
        return acc;
      }, {} as LocationHoursMap);
      console.log(this.sortedHours);
      this.columns = this.distributeToColumns(this.sortedHours, 12);
      console.log(this.columns);
    }
  }

  distributeToColumns(
    locationMap: LocationHoursMap,
    maxPerCol: number
  ): Column[] {
    /**
     * Splits the locations in locationMap into enough columns with no more than
     * maxPerCol rows per column. This is intended to be used when generating the HTML
     * to paginate the hours.
     *
     * Note that a row is defined as either an office hour entry or the dividing bar between 2 locations
     *
     * @input locationMap: The location based map of the Office Hours
     * @input maxPerCol: The max amount of office hours objects to have in one column
     * @returns Column[]: Column objects containing the locations to display
     */

    // Get each location and tally the amount of office hours at each one, then sort descending size
    const locationSizes = Object.entries(locationMap)
      .map(([location, hours]) => ({ location: location, size: hours.length }))
      .sort((a, b) => b.size - a.size);

    // Validate that no single location has over the maxOfficeHours amout
    if (locationSizes[0].size > maxPerCol) {
      throw new Error(
        `Location ${locationSizes[0].location} has ${locationSizes[0].size} office hours which is more than the max of ${maxPerCol} per display column.`
      );
    }

    const cols: Column[] = [];

    // Starting with the largest location, place into buckets
    locationSizes.forEach(({ location, size }) => {
      let colFound = false;

      // Look for column that we can place this location into
      for (const col of cols) {
        if (col.totalHours + size + 1 <= maxPerCol) {
          col.locations.push(location);
          col.totalHours += size + 1; // + 1 is for the dividing bar between locations
          colFound = true;
          break;
        }
      }

      // Create one if we didn't find one
      if (!colFound) {
        cols.push({
          locations: [location],
          totalHours: size
        });
      }
    });

    return cols;
  }
}
