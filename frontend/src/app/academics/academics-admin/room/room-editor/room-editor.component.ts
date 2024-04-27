/**
 * The Room editor page enables the administrator to add and edit
 * rooms.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023
 * @license MIT
 */

import { Component, inject } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  CanActivateFn,
  Route,
  Router,
  RouterStateSnapshot
} from '@angular/router';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { PermissionService } from 'src/app/permission.service';
import { profileResolver } from 'src/app/profile/profile.resolver';
import {
  roomResolver,
  termResolver
} from 'src/app/academics/academics.resolver';
import { Room, Term } from 'src/app/academics/academics.models';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AcademicsService } from 'src/app/academics/academics.service';
import { Profile } from 'src/app/models.module';
import { DatePipe } from '@angular/common';

const canActivateEditor: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  /** Determine if page is viewable by user based on permissions */

  let id: string = route.params['id'];

  if (id === 'new') {
    return inject(PermissionService).check('room.create', 'room');
  } else {
    return inject(PermissionService).check('room.update', `room/${id}`);
  }
};
@Component({
  selector: 'app-room-editor',
  templateUrl: './room-editor.component.html',
  styleUrls: ['./room-editor.component.css']
})
export class RoomEditorComponent {
  /** Route information to be used in the Routing Module */
  public static Route: Route = {
    path: 'room/edit/:id',
    component: RoomEditorComponent,
    title: 'Room Editor',
    canActivate: [canActivateEditor],
    resolve: {
      profile: profileResolver,
      room: roomResolver
    }
  };

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile | null = null;

  /** Store the room.  */
  public room: Room;

  /** Store the room id. */
  roomId: string = 'new';

  /** Add validators to the form */
  id = new FormControl('', [Validators.required]);
  nickname = new FormControl('', [Validators.required]);
  building = new FormControl('', [Validators.required]);
  roomName = new FormControl('', [Validators.required]);
  capacity = new FormControl(0, [Validators.required]);
  reservable = new FormControl(false, [Validators.required]);
  description = new FormControl('', [Validators.required]);

  /** Room Editor Form */
  public roomForm = this.formBuilder.group({
    id: this.id,
    nickname: this.nickname,
    building: this.building,
    room: this.roomName,
    capacity: this.capacity,
    reservable: this.reservable,
    description: this.description
  });

  /** Constructs the room editor component */
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar,
    private academicsService: AcademicsService,
    private datePipe: DatePipe
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      profile: Profile;
      room: Room;
    };
    this.profile = data.profile;
    this.room = data.room;

    /** Get id from the url */
    this.roomId = this.route.snapshot.params['id'];

    /** Set room form data */
    this.roomForm.setValue({
      id: this.room.id,
      nickname: this.room.nickname,
      building: this.room.building,
      room: this.room.room,
      capacity: this.room.capacity,
      reservable: this.room.reservable,
      description: this.room.description
    });
  }

  /** Event handler to handle submitting the Update Term Form.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.roomForm.valid) {
      Object.assign(this.room, this.roomForm.value);

      if (this.roomId == 'new') {
        this.academicsService.createRoom(this.room).subscribe({
          next: (room) => this.onSuccess(room),
          error: (err) => this.onError(err)
        });
      } else {
        this.academicsService.updateRoom(this.room).subscribe({
          next: (room) => this.onSuccess(room),
          error: (err) => this.onError(err)
        });
      }
    }
  }

  /** Opens a confirmation snackbar when a course is successfully updated.
   * @returns {void}
   */
  private onSuccess(room: Room): void {
    this.router.navigate(['/academics/admin/room']);

    let message: string =
      this.roomId === 'new' ? 'Room Created' : 'Room Updated';

    this.snackBar.open(message, '', { duration: 2000 });
  }

  /** Opens a snackbar when there is an error updating a room.
   * @returns {void}
   */
  private onError(err: any): void {
    let message: string =
      this.roomId === 'new'
        ? 'Error: Room Not Created'
        : 'Error: Room Not Updated';

    this.snackBar.open(message, '', {
      duration: 2000
    });
  }
}
