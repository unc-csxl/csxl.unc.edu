import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, ReplaySubject, Subject, map } from 'rxjs';
import { CoworkingStatus, CoworkingStatusJSON, parseCoworkingStatusJSON } from './coworking.models';


@Injectable({
    providedIn: 'root'
})
export class CoworkingService { 

    private status: Subject<CoworkingStatus> = new ReplaySubject(1);
    public status$: Observable<CoworkingStatus>;

    public constructor(protected http: HttpClient) {
        this.status$ = this.status.asObservable();
    }

    public pullStatus(): void {
        this.http.get<CoworkingStatusJSON>("/api/coworking/status")
            .pipe(map(parseCoworkingStatusJSON))
            .subscribe(status => this.status.next(status));
    }
}