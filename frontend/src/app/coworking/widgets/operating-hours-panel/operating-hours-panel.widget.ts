import { Component, Input } from '@angular/core';
import { OperatingHours } from 'src/app/coworking/coworking.models';

@Component({
  selector: 'coworking-operating-hours-panel',
  templateUrl: './operating-hours-panel.widget.html',
  styleUrls: ['./operating-hours-panel.widget.css']
})
export class CoworkingHoursCard {
  @Input() operatingHours!: OperatingHours[];
  @Input() openOperatingHours?: OperatingHours;
}
