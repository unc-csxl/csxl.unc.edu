import { Component, Input, OnInit } from '@angular/core';
import { Reservation } from '../../coworking.models';

@Component({
    selector: 'coworking-reservation-card',
    templateUrl: './coworking-reservation-card.html',
    styleUrls: ['./coworking-reservation-card.css']
})
export class CoworkingReservationCard implements OnInit {

    @Input() reservation!: Reservation;

    ngOnInit(): void { }

    checkinDeadline(reservationStart: Date): Date {
        return new Date(reservationStart.getTime() + (10 * 60 * 1000));
    }

}