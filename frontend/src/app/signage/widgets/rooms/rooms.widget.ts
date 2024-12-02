import { Component, OnInit, Input } from '@angular/core';
import { SignageService } from '../../signage.service';

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
