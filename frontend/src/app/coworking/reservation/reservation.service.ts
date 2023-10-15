import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, map, shareReplay } from "rxjs";
import { Reservation, ReservationJSON, parseReservationJSON } from "../coworking.models";
import { RxReservation } from "./rx-reservation";

@Injectable({
    providedIn: 'root'
})
export class ReservationService {

    private reservations: Map<number, RxReservation> = new Map();

    constructor(private http: HttpClient) { }

    get(id: number): Observable<Reservation> {
        let reservation = this.reservations.get(id);
        if (reservation === undefined) {
            let loader = this.http.get<ReservationJSON>(`/api/coworking/reservation/${id}`)
                .pipe(map(parseReservationJSON), shareReplay({ windowTime: 1000, refCount: true }));
            reservation = new RxReservation(loader);
            this.reservations.set(id, reservation);
        }
        reservation.load();
        return reservation.value$;
    }

}