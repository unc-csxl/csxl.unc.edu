import { COMPILER_OPTIONS, Component, OnInit } from '@angular/core';
import { ReservationTableService } from '../../room-reservation/reservation-table.service';
import { Subscription, max, Observable, throwError, catchError } from 'rxjs';
import { Router } from '@angular/router';
import {
  Reservation,
  ReservationRequest,
  TableCell
} from 'src/app/coworking/coworking.models';
import { RoomReservationService } from '../../room-reservation/room-reservation.service';
import { CloseScrollStrategy } from '@angular/cdk/overlay';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'room-reservation-table',
  templateUrl: './room-reservation-table.widget.html',
  styleUrls: ['./room-reservation-table.widget.css']
})
export class RoomReservationWidgetComponent {
  timeSlots = [
    '10:00AM <br> to<br> 10:30AM',
    '10:30AM <br> to<br> 11:00AM',
    '11:00AM <br> to<br> 11:30AM',
    '11:30AM <br> to<br> 12:00PM',
    '12:00PM <br> to<br> 12:30PM',
    '12:30PM <br> to<br>  1:00PM',
    ' &nbsp;1:00PM&nbsp;  <br>  to <br>  &nbsp;1:30PM&nbsp;',
    ' &nbsp;1:30PM&nbsp;  <br>  to <br>  &nbsp;2:00PM&nbsp;',
    ' &nbsp;2:00PM&nbsp;  <br>  to <br>  &nbsp;2:30PM&nbsp;',
    ' &nbsp;2:30PM&nbsp;  <br>  to <br>  &nbsp;3:00PM&nbsp;',
    ' &nbsp;3:00PM&nbsp;  <br>  to <br>  &nbsp;3:30PM&nbsp;',
    ' &nbsp;3:30PM&nbsp;  <br>  to <br>  &nbsp;4:00PM&nbsp;',
    ' &nbsp;4:00PM&nbsp;  <br>  to <br>  &nbsp;4:30PM&nbsp;',
    ' &nbsp;4:30PM&nbsp;  <br>  to <br>  &nbsp;5:00PM&nbsp;',
    ' &nbsp;5:00PM&nbsp;  <br>  to <br>  &nbsp;5:30PM&nbsp;',
    ' &nbsp;5:30PM&nbsp;  <br>  to <br>  &nbsp;6:00PM&nbsp;'
  ];

  //- Reservations Map
  reservationsMap: Record<string, number[]> = {};

  //- Select Button enabled
  selectButton: boolean = false;

  //- Selected Date
  selectedDate: string = '';
  // private subscription: Subscription;
  Object: any;
  subscription: Subscription;
  cellPropertyMap = ReservationTableService.CellPropertyMap;

  snackBarOptions: Object = {
    duration: 8000
  };

  constructor(
    protected reservationTableService: ReservationTableService,
    private router: Router,
    private roomReservationService: RoomReservationService,
    protected snackBar: MatSnackBar
  ) {
    this.reservationTableService.setSelectedDate(
      this.reservationTableService.setMinDate().toDateString()
    );
    this.subscription = this.reservationTableService.selectedDate$.subscribe(
      (selectedDate) => {
        this.selectedDate = selectedDate;
        this.getReservationsByDate(new Date(selectedDate));
      }
    );
  }

  getReservationsByDate(date: Date) {
    this.reservationTableService.getReservationsForRoomsByDate(date).subscribe(
      (result) => {
        this.reservationsMap = result;
      },
      (error) => {
        // Handle the error here
        this.snackBar.open(
          'Error fetching reservations',
          'Close',
          this.snackBarOptions
        );
        console.error('Error fetching reservations:', error);
      }
    );
  }

  //- Array to store information about selected cells, where each element is an object
  //- with 'key' representing the room number and 'index' representing the time interval.
  selectedCells: TableCell[] = [];

  /**
   * Toggles the color of a cell in the reservations map and manages selected cells.
   *
   * @param {string} key - The key representing the room in the reservations map.
   * @param {number} index - The index representing the time slot in the reservations map.
   * @returns {void} The method does not return a value.
   */
  toggleCellColor(key: string, index: number): void {
    const isSelected =
      this.reservationsMap[key][index] ===
      ReservationTableService.CellEnum.RESERVING;

    if (isSelected) {
      this.reservationTableService.deselectCell(key, index, this);
    } else {
      this.reservationTableService.selectCell(key, index, this);
    }

    this.selectButtonToggle();
  }

  //- Check if at least one time slot selected
  selectButtonToggle(): void {
    this.selectButton = Object.values(this.reservationsMap).some(
      (timeSlotsForRow) =>
        timeSlotsForRow.includes(ReservationTableService.CellEnum.RESERVING)
    );
  }

  /**
   * Initiates the process of drafting a reservation based on the current state
   * of the reservations map and the selected date.
   *
   * @throws {Error} If there is an exception during the drafting process.
   *
   * @remarks
   * The method calls the 'draftReservation' service method and handles the response:
   * - If the reservation is successfully drafted, the user is navigated to the
   *   confirmation page with the reservation data.
   * - If there is an error during the drafting process, the error is logged, and an
   *   alert with the error message is displayed to the user.
   *
   * @example
   * ```typescript
   * draftReservation();
   * ```
   */

  draftReservation() {
    const result = this.reservationTableService.draftReservation(
      this.reservationsMap,
      this.selectedDate
    );
    result.subscribe(
      (reservation: Reservation) => {
        // Navigate with the reservation data
        this.router.navigateByUrl(
          `/coworking/confirm-reservation/${reservation.id}`
        );
      },
      (error) => {
        // Handle errors here
        console.error('Error drafting reservation', error);
        this.snackBar.open(error.error.detail, 'Close', this.snackBarOptions);
      }
    );
  }

  /**
   * Setter for the reservations map to set the state of a timeslot to reserving.
   * @param key room id for reservationsMap.
   * @param index index of the timeslot to change the state of.
   */
  public setSlotReserving(key: string, index: number) {
    this.reservationsMap[key][index] =
      ReservationTableService.CellEnum.RESERVING;
  }

  /**
   * Setter for the reservations map to set the state of a timeslot to reserved.
   * @param key room id for reservationsMap.
   * @param index index of the timeslot to change the state of.
   */
  public setSlotAvailable(key: string, index: number) {
    this.reservationsMap[key][index] =
      ReservationTableService.CellEnum.AVAILABLE;
  }
}
