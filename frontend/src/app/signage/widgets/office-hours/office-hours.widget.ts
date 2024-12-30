/**
 * Office Hours Widget to Display all currently active office hours, their locations, and queue length
 *
 * @author Andrew Lockard <andrew.lockard15@gmail.com>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { SignageOfficeHours } from '../../signage.model';

type LocationHoursMap = { [location: string]: number[] }; // maps locations to index of the officeHours input

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
  columns_to_show: number[] = []; // Index of the columns array

  ngOnChanges(changes: SimpleChanges): void {
    if (
      changes['officeHours'] &&
      // Compare old vs new values to see if there is a change other than queue length
      (changes['officeHours'].previousValue === undefined ||
        this.test_OH_difference(
          changes['officeHours'].currentValue,
          changes['officeHours'].previousValue
        ))
    ) {
      this.sortedHours = this.officeHours.reduce((acc, curr, ind) => {
        if (!acc[curr.location]) {
          acc[curr.location] = [];
        }

        // Add the current's index to it's correct location list
        acc[curr.location].push(ind);
        return acc;
      }, {} as LocationHoursMap);
      console.log(this.sortedHours);
      this.columns = this.distributeToColumns(this.sortedHours, 10);
      console.log(this.columns);
      // TODO: Need to reset pagination since columns may be different
    }
  }

  rotate_columns() {
    console.log('TEST');
  }

  private test_OH_difference(
    oh1: SignageOfficeHours[],
    oh2: SignageOfficeHours[]
  ): boolean {
    /**
     * Tests to see if the two differencce office hours arrays are differing in anything but the queued length
     *
     * @input oh1/oh2 - lists of SignageOfficeHours that will be compared. !NOTE: These must be sorted by increasing id
     * @returns boolean - True if the lists are different in something other than queued length
     */

    if (oh1.length !== oh2.length) {
      return true;
    }

    for (let i = 0; i < oh1.length; i++) {
      if (
        oh1[i].id !== oh2[i].id ||
        oh1[i].course !== oh2[i].course ||
        oh1[i].location !== oh2[i].location
      ) {
        return true;
      }
    }
    return false;
  }

  private distributeToColumns(
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
    if (locationSizes[0].size + 1 > maxPerCol) {
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
          totalHours: size + 1
        });
      }
    });

    return cols;
  }
}
