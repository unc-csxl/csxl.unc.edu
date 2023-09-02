import { HttpClient } from '@angular/common/http';
import { Injectable, OnDestroy, OnInit } from '@angular/core';
import { Observable, ReplaySubject, Subject, Subscription, first, map, tap } from 'rxjs';
import { CoworkingStatus, CoworkingStatusJSON, Reservation, ReservationJSON, ReservationRequest, Seat, SeatAvailability, parseCoworkingStatusJSON, parseReservationJSON } from './coworking.models';
import { ProfileService } from '../profile/profile.service';
import { Profile } from '../models.module';

const ONE_HOUR = 60 * 60 * 1000;

// class ReactiveValue<T> implements OnDestroy {
//     private stream: Subject<T> = new ReplaySubject(1);
//     public stream$: Observable<T> = this.stream.asObservable();
//     private last!: T;

//     ngOnDestroy(): void {

//     }
// }


@Injectable({
    providedIn: 'root'
})
export class CoworkingService implements OnDestroy {

    private status: Subject<CoworkingStatus> = new ReplaySubject(1);
    public status$: Observable<CoworkingStatus>;
    private lastStatus!: CoworkingStatus;
    private lastStatusSubscription: Subscription;

    private profile: Profile | undefined;
    private profileSubscription!: Subscription;

    public constructor(protected http: HttpClient, protected profileSvc: ProfileService) {
        this.status$ = this.status.asObservable();
        this.lastStatusSubscription = this.status$.subscribe(status => this.lastStatus = status);

        this.profileSubscription = this.profileSvc.profile$.subscribe(profile => this.profile = profile);
    }

    ngOnDestroy(): void {
        this.profileSubscription.unsubscribe();
    }

    public pollStatus(): void {
        this.http.get<CoworkingStatusJSON>("/api/coworking/status")
            .pipe(map(parseCoworkingStatusJSON))
            .subscribe(status => this.status.next(status));
    }

    draftReservation(seatSelection: SeatAvailability[]) {
        if (this.profile === undefined) { throw new Error("Only allowed for logged in users."); }

        let start = seatSelection[0].availability[0].start;
        let end = new Date(start.getTime() + ONE_HOUR);

        return this.http.post<ReservationJSON>("/api/coworking/reservation", {
            users: [this.profile],
            seats: seatSelection.map(seatAvailability => { return { "id": seatAvailability.id } }),
            start,
            end
        }).pipe(
            /* Is there a cleaner way of doing this kind of update of a ReplaySubject? */
            tap(reservation => {
                this.status$
                    .pipe(first())
                    .subscribe(currentStatus => {
                        let nextStatus = Object.assign({}, currentStatus);
                        nextStatus.my_reservations.unshift(parseReservationJSON(reservation));
                        this.status.next(nextStatus);
                    });
            })
        );
    }

    confirmReservation(reservation: Reservation) {
        this.http.put<ReservationJSON>(`/api/coworking/reservation/${reservation.id}`, { id: reservation.id, state: "CONFIRMED" }).subscribe((updatedReservation) => {
            this.status$
                .pipe(first())
                .subscribe(currentStatus => {
                    let nextStatus = Object.assign({}, currentStatus);
                    nextStatus.my_reservations = nextStatus.my_reservations.map(reservation => {
                        if (reservation.id === updatedReservation.id) {
                            return parseReservationJSON(updatedReservation);
                        } else {
                            return reservation;
                        }
                    });
                    this.status.next(nextStatus);
                });
        });
    }

    cancelReservation(reservation: Reservation) {
        this.http.delete<ReservationJSON>(`/api/coworking/reservation/${reservation.id}`).subscribe((cancelledReservation => {
            this.status$
                .pipe(first())
                .subscribe(currentStatus => {
                    let nextStatus = Object.assign({}, currentStatus);
                    nextStatus.my_reservations = nextStatus.my_reservations.filter(reservation => reservation.id != cancelledReservation.id)
                    this.status.next(nextStatus);
                });
        }));
    }
}