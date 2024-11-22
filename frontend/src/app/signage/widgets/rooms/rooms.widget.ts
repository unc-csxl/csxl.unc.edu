import { Component, OnInit } from '@angular/core';
import { SignageService } from '../../signage.service';

@Component({
  selector: 'rooms',
  templateUrl: './rooms.widget.html',
  styleUrls: ['./rooms.widget.css']
})
export class RoomsWidget implements OnInit {
  availableRooms: string[] = [];
  allRooms: string[] = [
    'SN139',
    'SN144',
    'SN146',
    'SN135',
    'SN137',
    'SN141',
    'SN147'
  ];

  constructor(private signageService: SignageService) {}

  ngOnInit(): void {
    this.signageService.getFastData().subscribe((data) => {
      this.availableRooms = data.available_rooms;
    });
  }

  isRoomAvailable(room: string): boolean {
    return this.availableRooms.includes(room);
  }
}
