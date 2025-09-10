/**
 * The Rooms Card displays which rooms are currently available to be reserved.
 *
 * @author Will Zahrt <wzahrt@unc.edu>
 * @author Andrew Lockard <andrew.lockard15@gmail.com>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { AvailabeRoom } from '../../signage.model';

@Component({
    selector: 'rooms',
    templateUrl: './rooms.widget.html',
    styleUrls: ['./rooms.widget.css'],
    standalone: false
})
export class RoomsWidget {
  @Input() availableRooms: AvailabeRoom[] = [];

  pairingRooms = [AvailabeRoom.SN139, AvailabeRoom.SN144, AvailabeRoom.SN146];
  smallGroupRooms = [AvailabeRoom.SN135, AvailabeRoom.SN137];
  largeGroupRooms = [AvailabeRoom.SN141, AvailabeRoom.SN147];

  isRoomAvailable(room: AvailabeRoom): boolean {
    return this.availableRooms.includes(room);
  }

  toRoomName(room: AvailabeRoom): string {
    return AvailabeRoom[room];
  }
}
