import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { Profile, ProfileService, Permission } from './profile/profile.service';


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
                    return this.hasPermission(profile.permissions, action, resource);
                }
            })
        );
    }

    private hasPermission(permissions: Permission[], action: string, resource: string) {
        let permission = permissions.find((p) => this.checkPermission(p, action, resource));
        return permission !== undefined;
    }

    private checkPermission(permission: Permission, action: string, resource: string) {
        let actionRegExp = this.expandPattern(permission.action);
        if (actionRegExp.test(action)) {
            let resourceRegExp = this.expandPattern(permission.resource);
            return resourceRegExp.test(resource);
        } else {
            return false;
        }
    }

    private expandPattern(pattern: string): RegExp {
        return new RegExp(`^${pattern.replaceAll('*', '.*')}$`);
    }

}