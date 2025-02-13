/**
 * The Rooms Card displays which rooms are currently available to be reserved.
 *
 * @author Will Zahrt <wzahrt@unc.edu>
 * @author Andrew Lockard <andrew.lockard15@gmail.com>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';

@Component({
  selector: 'rooms',
  templateUrl: './rooms.widget.html',
  styleUrls: ['./rooms.widget.css']
})
export class RoomsWidget {
  @Input() availableRooms: string[] = [];
  allRooms: string[] = [
    'SN139',
    'SN144',
    'SN146',
    'SN135',
    'SN137',
    'SN141',
    'SN147'
  ];

  constructor() {}

  isRoomAvailable(room: string): boolean {
    return this.availableRooms.includes(room);
  }
}
