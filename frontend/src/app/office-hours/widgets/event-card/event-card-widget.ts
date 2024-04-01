import { Component } from '@angular/core';
import { flushMicrotasks } from '@angular/core/testing';

@Component({
  selector: 'event-card-widget',
  templateUrl: './event-card-widget.html',
  styleUrls: ['./event-card-widget.css']
})
export class EventCard {
  constructor() {}
}
