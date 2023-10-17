import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subscription, map, tap } from 'rxjs';
import { CoworkingStatus, CoworkingStatusJSON, Reservation, ReservationJSON, SeatAvailability, parseCoworkingStatusJSON, parseReservationJSON } from './coworking.models';
import { ProfileService } from '../profile/profile.service';
import { Profile } from '../models.module';
import { RxCoworkingStatus } from './rx-coworking-status';

const ONE_HOUR = 60 * 60 * 1000;

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

    pollStatus(): void {
        this.http.get<CoworkingStatusJSON>("/api/coworking/status")
            .pipe(map(parseCoworkingStatusJSON))
            .subscribe(status => this.status.set(status));
    }

    draftReservation(seatSelection: SeatAvailability[]) {
        if (this.profile === undefined) { throw new Error("Only allowed for logged in users."); }

        let start = seatSelection[0].availability[0].start;
        let end = new Date(start.getTime() + ONE_HOUR);
        let reservation = {
            users: [this.profile],
            seats: seatSelection.map(seatAvailability => { return { "id": seatAvailability.id } }),
            start,
            end
        };

        return this.http.post<ReservationJSON>("/api/coworking/reservation", reservation).pipe(map(parseReservationJSON));
    }

    // confirmReservation(reservation: Reservation) {
    //     let reservationPartial = { id: reservation.id, state: "CONFIRMED" };
    //     this.http.put<ReservationJSON>(`/api/coworking/reservation/${reservation.id}`, reservationPartial)
    //         .subscribe((updatedReservation) => this.status.updateReservation(parseReservationJSON(updatedReservation)));
    // }

    // cancelReservation(reservation: Reservation) {
    //     this.http.delete<ReservationJSON>(`/api/coworking/reservation/${reservation.id}`).subscribe((cancelledReservation => {
    //         this.status.removeReservation(parseReservationJSON(cancelledReservation))
    //     }));
    // }

}