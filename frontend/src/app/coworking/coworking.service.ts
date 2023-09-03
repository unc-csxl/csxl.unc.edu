import { HttpClient } from '@angular/common/http';
import { Injectable, OnDestroy, OnInit } from '@angular/core';
import { Observable, ReplaySubject, Subject, Subscription, first, map, tap } from 'rxjs';
import { CoworkingStatus, CoworkingStatusJSON, Reservation, ReservationJSON, ReservationRequest, Seat, SeatAvailability, parseCoworkingStatusJSON, parseReservationJSON } from './coworking.models';
import { ProfileService } from '../profile/profile.service';
import { Profile } from '../models.module';

const ONE_HOUR = 60 * 60 * 1000;

abstract class RxObject<T> {

    protected value!: T;
    protected subject: Subject<T> = new ReplaySubject(1);

    public value$: Observable<T> = this.subject.asObservable();

    set(value: T): void {
        this.value = value;
        this.notify();
    }

    protected notify() {
        this.subject.next(this.value);
    }

}

class RxCoworkingStatus extends RxObject<CoworkingStatus> {

    pushReservation(reservation: Reservation): void {
        this.value.my_reservations.push(reservation);
        this.notify();
    }

    updateReservation(reservation: Reservation): void {
        this.value.my_reservations = this.value.my_reservations.map((r) => {
            return r.id !== reservation.id ? r : reservation;
        });
        this.notify();
    }

    removeReservation(reservationToRemove: Reservation): void {
        this.value.my_reservations = this.value.my_reservations.filter(reservation => reservationToRemove.id !== reservation.id);
        this.notify();
    }

}


@Injectable({
    providedIn: 'root'
})
export class CoworkingService {

    private status: RxCoworkingStatus = new RxCoworkingStatus();
    public status$: Observable<CoworkingStatus> = this.status.value$;

    private profile: Profile | undefined;
    private profileSubscription!: Subscription;

    public constructor(protected http: HttpClient, protected profileSvc: ProfileService) {
        this.profileSubscription = this.profileSvc.profile$.subscribe(profile => this.profile = profile);
    }

    ngOnDestroy(): void {
        this.profileSubscription.unsubscribe();
    }

    public pollStatus(): void {
        this.http.get<CoworkingStatusJSON>("/api/coworking/status")
            .pipe(map(parseCoworkingStatusJSON))
            .subscribe(status => this.status.set(status));
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
            tap(reservation => this.status.pushReservation(parseReservationJSON(reservation)))
        );
    }

    confirmReservation(reservation: Reservation) {
        this.http.put<ReservationJSON>(`/api/coworking/reservation/${reservation.id}`, { id: reservation.id, state: "CONFIRMED" })
            .subscribe((updatedReservation) => this.status.updateReservation(parseReservationJSON(updatedReservation)));
    }

    cancelReservation(reservation: Reservation) {
        this.http.delete<ReservationJSON>(`/api/coworking/reservation/${reservation.id}`).subscribe((cancelledReservation => {
            this.status.removeReservation(parseReservationJSON(cancelledReservation))
        }));
    }
}