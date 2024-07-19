import { Component, Input } from '@angular/core';
import { EventOverview, RegistrationType } from '../../event.model';

@Component({
  selector: 'new-event-card',
  templateUrl: './event-card.widget.html',
  styleUrl: './event-card.widget.css'
})
export class EventCardWidget {
  registrationType = RegistrationType;
  @Input() event!: EventOverview;
}
