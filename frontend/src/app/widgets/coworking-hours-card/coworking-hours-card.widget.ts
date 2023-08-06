import { Component, Input } from '@angular/core';
import { OperatingHours } from 'src/app/coworking/coworking.models';

@Component({
    selector: 'coworking-hours-card',
    templateUrl: './coworking-hours-card.widget.html',
    styleUrls: ['./coworking-hours-card.widget.css']
})
export class CoworkingHoursCard {

    @Input() operatingHours!: OperatingHours[];
    @Input() openOperatingHours?: OperatingHours;

}