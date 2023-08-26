import { HttpClient } from '@angular/common/http';
import { Injectable, OnDestroy, OnInit } from '@angular/core';
import { Observable, ReplaySubject, Subject, Subscription, map } from 'rxjs';
import { CoworkingStatus, CoworkingStatusJSON, ReservationRequest, SeatAvailability, parseCoworkingStatusJSON } from './coworking.models';
import { ProfileService } from '../profile/profile.service';
import { Profile } from '../models.module';


@Injectable({
    providedIn: 'root'
})
export class CoworkingService implements OnDestroy {

    private status: Subject<CoworkingStatus> = new ReplaySubject(1);
    public status$: Observable<CoworkingStatus>;

    private profile: Profile | undefined;
    private profileSubscription!: Subscription;

    public constructor(protected http: HttpClient, protected profileSvc: ProfileService) {
        this.status$ = this.status.asObservable();
        this.profileSubscription = this.profileSvc.profile$.subscribe(profile => this.profile = profile);
    }

    ngOnDestroy(): void {
        this.profileSubscription.unsubscribe();
        console.log('destroy');
    }

    public pullStatus(): void {
        this.http.get<CoworkingStatusJSON>("/api/coworking/status")
            .pipe(map(parseCoworkingStatusJSON))
            .subscribe(status => this.status.next(status));
    }

    draftReservation(seatSelection: SeatAvailability[]) {
        if (this.profile === undefined) { throw new Error("Only allowed for logged in users."); }
        return this.http.post<ReservationRequest>("/api/coworking/reservation", {
            users: [this.profile],
            seats: seatSelection,
            start: seatSelection[0].availability[0].start,
            end: new Date(seatSelection[0].availability[0].start.getMilliseconds() + 60000)
        });
    }
}