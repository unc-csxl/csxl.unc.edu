/**
 * Office Hours Widget to display all currently active office hours, their locations, and queue length
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
  displayOfficeHours!: SignageOfficeHours[]; // Hours that are on display currently
  sortedHours: LocationHoursMap = {};
  columns: Column[] = [];
  columnsToShow: number[] = []; // Index of the columns array
  private updater: undefined | (() => void) = undefined; // sets the new sortedHours and columns on change

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['officeHours']) {
      // Compare old vs new values to see if there is a change other than queue length
      if (
        this.displayOfficeHours === undefined ||
        this.testOHDifference(
          changes['officeHours'].currentValue,
          this.displayOfficeHours
        )
      ) {
        let newSortedHours: LocationHoursMap;
        let newColumns: Column[];

        // Handle no current office hours case
        if (changes['officeHours'].currentValue.length === 0) {
          newSortedHours = {};
          newColumns = [];
        } else {
          newSortedHours = this.officeHours.reduce((acc, curr, ind) => {
            if (!acc[curr.location]) {
              acc[curr.location] = [];
            }

            // Add the current's index to it's correct location list
            acc[curr.location].push(ind);
            return acc;
          }, {} as LocationHoursMap);

          newColumns = this.distributeToColumns(newSortedHours, 8);
        }

        // If we currently have more than 2 columns, we will run this update in sync with the page spinner
        if (this.columns.length > 2) {
          this.updater = () => {
            this.displayOfficeHours = this.officeHours;
            this.sortedHours = newSortedHours;
            this.columns = newColumns;
            this.resetDisplayColumns(newColumns.length);
          };
        } else {
          this.displayOfficeHours = this.officeHours;
          this.sortedHours = newSortedHours;
          this.columns = newColumns;
          this.resetDisplayColumns(newColumns.length);
        }
      } else {
        // Update only queue values so we can just update the displayOfficeHours
        this.displayOfficeHours = this.officeHours;
      }
    }
  }

  rotateColumns() {
    // If there is an update ready, run it
    if (this.updater) {
      this.updater();
      this.updater = undefined;
    } else {
      // Otherwise just shift all columns forward by 1 using circular logic
      this.columnsToShow[0] = (this.columnsToShow[0] + 1) % this.columns.length;
      this.columnsToShow[1] = (this.columnsToShow[0] + 1) % this.columns.length;
    }
  }

  private resetDisplayColumns(col_nums: number) {
    if (col_nums >= 2) {
      this.columnsToShow = [0, 1];
    } else if (col_nums === 1) {
      this.columnsToShow = [0];
    } else {
      this.columnsToShow = [];
    }
  }

  /**
   * Tests to see if the two different office hour arrays are differing in anything but the queued length
   *
   * @input oh1/oh2 - lists of SignageOfficeHours that will be compared. !NOTE: These must be sorted by increasing id
   * @returns boolean - True if the lists are different in something other than queued length
   */
  private testOHDifference(
    oh1: SignageOfficeHours[],
    oh2: SignageOfficeHours[]
  ): boolean {
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
  private distributeToColumns(
    locationMap: LocationHoursMap,
    maxPerCol: number
  ): Column[] {
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
        if (col.totalHours + size <= maxPerCol) {
          col.locations.push(location);
          col.totalHours += size; // + 1 is for the dividing bar between locations
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
