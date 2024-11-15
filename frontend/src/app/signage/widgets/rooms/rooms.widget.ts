import { Component } from '@angular/core';

@Component({
  selector: 'rooms',
  templateUrl: './rooms.widget.html',
  styleUrls: ['./rooms.widget.css']
})
export class RoomsWidget {
  /** Inputs and outputs go here */
  rooms: { [room: string]: boolean } = {
    SN139: false,
    SN144: false,
    SN146: false,
    SN135: false,
    SN137: false,
    SN141: false,
    SN147: false
  };

  /** Constructor */
  constructor() {}
}
