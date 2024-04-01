/**
 * The Rooms Admin page enables the administrator to add, edit,
 * and delete rooms.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023
 * @license MIT
 */

import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { AcademicsService } from '../../academics.service';
import { RxRoomList } from '../rx-academics-admin';
import { Observable } from 'rxjs';
import { Room } from '../../academics.models';

@Component({
  selector: 'app-admin-room',
  templateUrl: './admin-room.component.html',
  styleUrls: ['./admin-room.component.css']
})
export class AdminRoomComponent {
  public static Route = {
    path: 'room',
    component: AdminRoomComponent,
    title: 'Room Administration',
    canActivate: [permissionGuard('academics.term', '*')]
  };

  /** Rooms List */
  public rooms: RxRoomList = new RxRoomList();
  public rooms$: Observable<Room[]> = this.rooms.value$;

  public displayedColumns: string[] = ['name'];

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private academicsService: AcademicsService
  ) {
    academicsService.getRooms().subscribe((rooms) => {
      this.rooms.set(rooms);
    });
  }

  /** Event handler to open the Term Editor to create a new term */
  createRoom(): void {
    // Navigate to the term editor
    this.router.navigate(['academics', 'room', 'edit', 'new']);
  }

  /** Event handler to open the Room Editor to update a course
   * @param room: room to update
   */
  updateRoom(room: Room): void {
    // Navigate to the course editor
    this.router.navigate(['academics', 'room', 'edit', room.id]);
  }

  /** Delete a room object from the backend database table using the backend HTTP delete request.
   * @param room: room to delete
   * @param event: event to stop propagation
   * @returns void
   */
  deleteRoom(room: Room, event: Event): void {
    event.stopPropagation();
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this room?',
      'Delete'
    );
    confirmDelete.onAction().subscribe(() => {
      this.academicsService.deleteRoom(room).subscribe({
        next: () => {
          this.rooms.removeRoom(room);
          this.snackBar.open('This room has been deleted.', '', {
            duration: 2000
          });
        },
        error: () => {
          this.snackBar.open(
            'Delete failed because this room is being used elsewhere.',
            '',
            {
              duration: 2000
            }
          );
        }
      });
    });
  }
}
