import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { Profile, ProfileService } from './profile/profile.service';

@Injectable({
    providedIn: 'root'
})
export class PermissionService {

    private profile$: Observable<Profile | undefined>;

    constructor(profileService: ProfileService) {
        this.profile$ = profileService.profile$;
    }

    check(action: string, resource: string): Observable<boolean> {
        return this.profile$.pipe(
            map(profile => {
                if (profile === undefined) {
                    return false;
                } else {
                    if (profile.permissions.length === 0) {
                        return false;
                    }
                    return true;
                }
            })
        );
    }

}