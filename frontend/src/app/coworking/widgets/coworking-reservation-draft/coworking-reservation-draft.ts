import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Reservation } from '../../coworking.models';
import { Observable, map, timer } from 'rxjs';

@Component({
    selector: 'coworking-reservation-draft',
    templateUrl: './coworking-reservation-draft.html',
    styleUrls: ['./coworking-reservation-draft.css']
})
export class CoworkingReservationDraft implements OnInit {

    @Input() reservation!: Reservation;

    @Output() onCancel = new EventEmitter<Reservation>();

    @Output() onConfirm = new EventEmitter<Reservation>();

    private deadline!: number;
    timeout$!: Observable<string>;

    ngOnInit(): void {
        this.deadline = this.reservation.created_at.getTime() + 5 /* minutes */ * 60 /* seconds */ * 1000 /* milliseconds */;
        this.timeout$ = timer(0, 1000).pipe(map(() => {
            const now = (new Date().getTime())
            const delta = (this.deadline - now) / 1000 /* milliseconds */;
            if (delta > 60) {
                return Math.ceil(delta / 60) + " minutes";
            } else if (delta > 0) {
                return Math.ceil(delta) + " seconds";
            } else {
                this.onCancel.emit(this.reservation);
                return "Cancelling...";
            }
        }))
    }

    checkinDeadline(reservationStart: Date): Date {
        return new Date(reservationStart.getTime() + (10 * 60 * 1000));
    }

}