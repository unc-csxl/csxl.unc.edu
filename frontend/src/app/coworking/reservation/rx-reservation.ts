import { Injectable } from "@angular/core";
import { Reservation } from "../coworking.models";
import { RxObject } from "src/app/rx-object";
import { Observable, take } from "rxjs";

@Injectable()
export class RxReservation extends RxObject<Reservation> {

    constructor(private loader: Observable<Reservation>) {
        super();
    }

    load() {
        this.loader
            .pipe(take(1))
            .subscribe(reservation => this.set(reservation));
    }

}