import { Injectable } from "@angular/core";
import { RxReservation } from "./rx-reservation";
import { Observable, map, tap } from "rxjs";
import { Reservation, ReservationJSON, parseReservationJSON } from "../coworking.models";
import { HttpClient } from "@angular/common/http";

@Injectable()
export class ReservationService {

    private reservation: RxReservation;
    public reservation$: Observable<Reservation>;

    constructor(private httpClient: HttpClient) {
        this.reservation = new RxReservation();
        this.reservation$ = this.reservation.value$;
    }

    get(id: number): Observable<Reservation> {
        return this.httpClient.get<ReservationJSON>(`/api/coworking/reservation/${id}`)
            .pipe(
                map(parseReservationJSON),
                tap(reservation => this.reservation.set(reservation))
            )
    }

}