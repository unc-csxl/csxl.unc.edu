/**
 * @author John Schachte, Aarjav Jain, Nick Wherthey, Matt Vu
 * @copyright 2024
 * @license MIT
 */

import { Component, EventEmitter } from '@angular/core';
import { ReservationTableService } from '../../room-reservation/reservation-table.service';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';
import {
  Reservation,
  TableCell,
  RoomDetails
} from 'src/app/coworking/coworking.models';
import { RoomReservationService } from '../../room-reservation/room-reservation.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { GroupReservation } from '../group-reservation-card/group-reservation-card.widget';
import { Profile } from 'src/app/models.module';
import { MatDialog } from '@angular/material/dialog';
import { PublicProfile } from 'src/app/profile/profile.service';

import { RoomCapacityDialogComponent } from '../room-dialogue/room-dialogue.component';

@Component({
  selector: 'room-reservation-table',
  templateUrl: './room-reservation-table.widget.html',
  styleUrls: ['./room-reservation-table.widget.css']
})
export class RoomReservationWidgetComponent {
  timeSlots: string[] = [];

  //- Reservations Map
  reservationsMap: Record<string, number[]> = {};

  //- Room Details
  roomDetailsArray: RoomDetails[] = [];

  //- Select Button enabled
  selectButton: boolean = false;

  operationStart: Date = new Date();

  //- Selected Date
  selectedDate: string = '';
  // private subscription: Subscription;
  Object: any;
  subscription: Subscription;
  cellPropertyMap = ReservationTableService.CellPropertyMap;

  snackBarOptions: Object = {
    duration: 8000
  };
  dialog: MatDialog;
  reservation: any;
  selectedUsers: PublicProfile[] = [];
  updateReservationsList: EventEmitter<any> = new EventEmitter<any>();

  constructor(
    protected reservationTableService: ReservationTableService,
    private router: Router,
    private roomReservationService: RoomReservationService,
    protected snackBar: MatSnackBar,
    dialog: MatDialog
  ) {
    this.dialog = dialog;
    this.reservationTableService.setSelectedDate(
      this.reservationTableService.setMinDate().toDateString()
    );
    this.subscription = this.reservationTableService.selectedDate$.subscribe(
      (selectedDate: string) => {
        this.selectedDate = selectedDate;
        this.getReservationsByDate(new Date(selectedDate));
      }
    );

    this.reservationTableService.getRoomInformation().subscribe((result) => {
      this.roomDetailsArray = result;
    });
  }

  getReservationsByDate(date: Date) {
    this.reservationTableService.getReservationsForRoomsByDate(date).subscribe(
      (result) => {
        this.reservationsMap = result.reserved_date_map;
        let end = new Date(result.operating_hours_end);
        this.operationStart = new Date(result.operating_hours_start);
        let slots = result.number_of_time_slots;

        this.timeSlots = this.reservationTableService.generateTimeSlots(
          this.operationStart,
          end,
          slots
        );
      },
      (error: Error) => {
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
      this.operationStart,
      this.selectedUsers
    );
    result.subscribe(
      (reservation: Reservation) => {
        // Navigate with the reservation data
        this.router.navigateByUrl(
          `/coworking/confirm-reservation/${reservation.id}`
        );
      },

      (error) => {
        let errorMessage = 'Unknown error';
        try {
          const errorObj = JSON.parse(error.message);
          errorMessage = errorObj.error.message;
        } catch (e) {
          errorMessage = error.message || 'Error occurred';
        }
        this.snackBar.open(errorMessage, 'Close', this.snackBarOptions);
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

  openMemberSelectionDialog(): void {
    const dialogRef = this.dialog.open(GroupReservation, {
      autoFocus: 'dialog',
      width: '500px',
      height: '280px',
      panelClass: 'custom-dialog-container',
      data: { selectedUsers: this.selectedUsers }
    });

    dialogRef.afterClosed().subscribe((selectedUsers: PublicProfile[]) => {
      if (selectedUsers) {
        this.selectedUsers = selectedUsers;
        console.log('Updated selected users:', this.selectedUsers);
        if (this.reservation) {
          this.reservation.users = selectedUsers;
          this.updateReservationsList.emit(this.reservation);
        }
      }
    });
  }
  getUserNames(users: Profile[]): string {
    return users
      .map((user) => `${user.first_name} ${user.last_name}`)
      .join(', ');
  }

  openDialog(roomId: string) {
    const room = this.roomDetailsArray.find((r) => r.id === roomId);
    if (room) {
      this.dialog.open(RoomCapacityDialogComponent, {
        width: '250px',
        data: {
          id: room.id,
          capacity: room.capacity,
          description: room.description
        }
      });
    }
  }

  getRoomCapacity(roomId: string): number | null {
    const room = this.roomDetailsArray.find((r) => r.id === roomId);
    return room ? room.capacity : null;
  }
}
