/**
 * @author John Schachte, Aarjav Jain, Nick Wherthey
 * @copyright 2023
 * @license MIT
 */

import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, Subscription } from 'rxjs';
import {
  Reservation,
  ReservationMapDetails,
  ReservationRequest,
  TableCell,
  TablePropertyMap
} from '../coworking.models';
import { ProfileService } from '../../profile/profile.service';
import { Profile } from '../../models.module';
import { RoomReservationWidgetComponent } from '../widgets/room-reservation-table/room-reservation-table.widget';

@Injectable({
  providedIn: 'root'
})
export class ReservationTableService {
  private selectedDateSubject = new BehaviorSubject<string>('');
  selectedDate$ = this.selectedDateSubject.asObservable();
  private profile: Profile | undefined;
  private profileSubscription!: Subscription;

  private EndingOperationalHour: number = 18;

  static readonly MAX_RESERVATION_CELL_LENGTH: number = 4; // rule for how long a reservation can be consecutively

  static readonly CellEnum = {
    AVAILABLE: 0,
    BOOKED: 1,
    RESERVING: 2,
    UNAVAILABLE: 3,
    SUBJECT_RESERVATION: 4
  } as const;

  //Add table cell states here
  static readonly CellPropertyMap: TablePropertyMap = {
    [ReservationTableService.CellEnum.AVAILABLE]: {
      backgroundColor: '#03691e',
      isDisabled: false
    },
    [ReservationTableService.CellEnum.BOOKED]: {
      backgroundColor: 'red',
      isDisabled: true
    },
    [ReservationTableService.CellEnum.RESERVING]: {
      backgroundColor: 'orange',
      isDisabled: false
    },
    [ReservationTableService.CellEnum.UNAVAILABLE]: {
      backgroundColor: '#4d4d4d',
      isDisabled: true
    },
    [ReservationTableService.CellEnum.SUBJECT_RESERVATION]: {
      backgroundColor: '#3479be',
      isDisabled: true
    }
  };

  constructor(
    private http: HttpClient,
    protected profileSvc: ProfileService
  ) {
    this.profileSubscription = this.profileSvc.profile$.subscribe(
      (profile) => (this.profile = profile)
    );
  }

  setSelectedDate(date: string) {
    this.selectedDateSubject.next(date);
  }

  //TODO Change route from ISO String to date object
  getReservationsForRoomsByDate(date: Date): Observable<ReservationMapDetails> {
    let params = new HttpParams().set('date', date.toISOString());
    return this.http.get<ReservationMapDetails>(
      `/api/coworking/room-reservation/`,
      { params }
    );
  }

  draftReservation(
    reservationsMap: Record<string, number[]>,
    operationStart: Date
  ): Observable<Reservation> {
    const selectedRoom: { room: string; availability: number[] } | null =
      this._findSelectedRoom(reservationsMap);

    if (!selectedRoom) throw new Error('No room selected');
    const reservationRequest: ReservationRequest = this._makeReservationRequest(
      selectedRoom!,
      operationStart
    );
    return this.makeDraftReservation(reservationRequest);
  }

  //TODO Draft Reservation method
  makeDraftReservation(
    reservationRequest: ReservationRequest
  ): Observable<Reservation> {
    return this.http.post<Reservation>(
      `/api/coworking/reservation`,
      reservationRequest
    );
  }

  /**
   * Deselects a cell in the reservations map and updates selected cells.
   *
   * @param {string} key - The key representing the room in the reservations map.
   * @param {number} index - The index representing the time slot in the reservations map.
   * @returns {void} The method does not return a value.
   * @public This method is intended for internal use.
   */
  public deselectCell(
    key: string,
    index: number,
    tableWidget: RoomReservationWidgetComponent
  ): void {
    tableWidget.setSlotAvailable(key, index);

    tableWidget.selectedCells = tableWidget.selectedCells.filter(
      (cell) => !(cell.key === key && cell.index === index)
    );

    const isAllAdjacent = this._areAllAdjacent(tableWidget.selectedCells);
    if (!isAllAdjacent) {
      tableWidget.selectedCells = this._updateAdjacentCells(index, tableWidget);
    }
  }

  /**
   * Selects a cell in the reservations map and updates selected cells.
   *
   * @param {string} key - The key representing the room in the reservations map.
   * @param {number} index - The index representing the time slot in the reservations map.
   * @returns {void} The method does not return a value.
   * @public This method is intended for internal use.
   */

  public selectCell(
    key: string,
    index: number,
    tableWidget: RoomReservationWidgetComponent
  ): void {
    const isAdjacentToAny = tableWidget.selectedCells.some(
      (cell: TableCell) => {
        return Math.abs(index - cell.index) <= 1 && key === cell.key;
      }
    );

    if (
      isAdjacentToAny &&
      tableWidget.selectedCells.length <
        ReservationTableService.MAX_RESERVATION_CELL_LENGTH
    ) {
      // If adjacent and within the maximum reservation length, select the cell
      tableWidget.setSlotReserving(key, index);

      tableWidget.selectedCells.push({ key, index });
    } else if (
      tableWidget.selectedCells.length >=
      ReservationTableService.MAX_RESERVATION_CELL_LENGTH
    ) {
      // If the maximum reservation length is exceeded, deselect all cells
      this._setAllAvailable(tableWidget);
      tableWidget.selectedCells = [{ key, index }]; // resetting selected cells to lone cell
      tableWidget.setSlotReserving(key, index);
    } else {
      // If not adjacent to any selected cells, deselect all and select the new cell
      this._setAllAvailable(tableWidget);
      tableWidget.selectedCells = [{ key, index }]; // resetting selected cells to lone cell
      tableWidget.setSlotReserving(key, index);
    }
  }

  _findSelectedRoom(
    reservationsMap: Record<string, number[]>
  ): { room: string; availability: number[] } | null {
    //- Finding the room with the selected cells (assuming only 1 row)
    const result = Object.entries(reservationsMap).find(
      ([id, availability]) => {
        return availability.includes(
          ReservationTableService.CellEnum.RESERVING
        );
      }
    );
    return result ? { room: result[0], availability: result[1] } : null;
  }

  _makeReservationRequest(
    selectedRoom: { room: string; availability: number[] },
    operationStart: Date
  ): ReservationRequest {
    const minIndex = selectedRoom?.availability.indexOf(
      ReservationTableService.CellEnum.RESERVING
    );
    const maxIndex = selectedRoom?.availability.lastIndexOf(
      ReservationTableService.CellEnum.RESERVING
    );
    const thirtyMinutes = 30 * 60 * 1000;
    const startDateTime = new Date(
      operationStart.getTime() + thirtyMinutes * minIndex
    );

    const endDateTime = new Date(
      operationStart.getTime() + thirtyMinutes * (maxIndex + 1)
    );

    return {
      users: [this.profile!],
      seats: [],
      room: { id: selectedRoom!.room },
      start: startDateTime,
      end: endDateTime
    };
  }

  /**
   * Makes all selected cells Available.
   * @param tableWidget RoomReservationWidgetComponent
   * @returns void
   * @private This method is intended for internal use.
   *
   */
  private _setAllAvailable(tableWidget: RoomReservationWidgetComponent): void {
    tableWidget.selectedCells.forEach((cell: TableCell) => {
      tableWidget.setSlotAvailable(cell.key, cell.index);
    });
  }

  /**
   * Checks if all currently selected cells are adjacent to each other.
   *
   * @returns {boolean} True if all selected cells are adjacent, false otherwise.
   * @private This method is intended for internal use.
   */

  private _areAllAdjacent(selectedCells: TableCell[]): boolean {
    return selectedCells.every((cell: TableCell, i) => {
      if (i < selectedCells.length - 1) {
        const nextCell = selectedCells[i + 1];
        return Math.abs(cell.index - nextCell.index) <= 1; // Check if the next cell is adjacent
      }
      return true; // Always return true for the last element
    });
  }

  /**
   * Updates adjacent cells based on the index of the selected cell.
   *
   * @param {number} index - The index representing the time slot in the reservations map.
   * @returns {void} The method does not return a value.
   * @private This method is intended for internal use.
   */

  private _updateAdjacentCells(
    index: number,
    tableWidget: RoomReservationWidgetComponent
  ): TableCell[] {
    // count if there are more cells on the left or on the right
    const leftFrom = this._countIfOnLeft(index, tableWidget.selectedCells);
    const rightFrom = tableWidget.selectedCells.length - leftFrom; // right and left counts are disjoint
    return this._filterCellsBasedOnIndex(
      tableWidget,
      index,
      leftFrom < rightFrom
    );
  }

  /**
   * Filters selected cells based on their index relative to a given index.
   *
   * @param tableWidget The RoomReservationWidgetComponent instance.
   * @param index The index to compare against.
   * @param filterBefore If true, filters out cells before the index; otherwise, filters out cells after the index.
   */
  private _filterCellsBasedOnIndex(
    tableWidget: RoomReservationWidgetComponent,
    index: number,
    filterBefore: boolean
  ): TableCell[] {
    return (
      tableWidget.selectedCells.filter((cell) => {
        if (filterBefore && cell.index < index) {
          tableWidget.setSlotAvailable(cell.key, cell.index);
          return false;
        } else if (!filterBefore && cell.index > index) {
          tableWidget.reservationsMap[cell.key][cell.index] =
            ReservationTableService.CellEnum.AVAILABLE;
          return false;
        }
        return true;
      }) ?? []
    );
  }

  /**
   * Counts the number of cells on the left of the selected cell.
   * @param index number
   * @param selectedCells TableCell[]
   * @returns number
   * @private This method is intended for internal use.
   */

  private _countIfOnLeft(index: number, selectedCells: TableCell[]): number {
    return selectedCells.reduce(
      (count, cell) => (cell.index < index ? (count += 1) : count),
      0
    );
  }

  setMaxDate(): Date {
    let result = new Date();
    result.setDate(result.getDate() + 7);
    return result;
  }

  setMinDate(): Date {
    let result = new Date();
    if (result.getHours() >= this.EndingOperationalHour) {
      result.setDate(result.getDate() + 1);
    }
    return result;
  }

  /**
   * Formats a date object into a string of the format 'HH:MMAM/PM'.
   *
   * @private
   * @param {Date} date - The date object to be formatted.
   * @returns {string} The formatted time string in 'HH:MMAM/PM' format.
   */
  private formatAMPM(date: Date): string {
    let hours = date.getHours();
    let minutes = date.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    const minutesStr = minutes < 10 ? '0' + minutes : minutes.toString();
    return `${hours}:${minutesStr}${ampm}`;
  }

  /**
   * Generates time slots between two dates in increments of thirty minutes, formatted as 'HH:MMA/PM <br> to <br> HH:MMPM'.
   *
   * @private
   * @param {Date} start - The start date and time for generating time slots.
   * @param {Date} end - The end date and time for the time slots.
   * @param {number} slots - The number of slots to generate.
   * @returns {string[]} An array of strings representing the time slots in 'HH:MMA/PM <br> to <br> HH:MMPM' format.
   */
  generateTimeSlots(start: Date, end: Date, slots: number): string[] {
    const timeSlots = [];
    const ThirtyMinutes = 30 * 60000; // Thirty minutes in milliseconds
    while (start < end) {
      let thirtyMinutesLater = new Date(start.getTime() + ThirtyMinutes);
      timeSlots.push(
        `${this.formatAMPM(start)} <br> to <br> ${this.formatAMPM(
          thirtyMinutesLater
        )}`
      );
      start = thirtyMinutesLater;
    }
    return timeSlots;
  }
}
