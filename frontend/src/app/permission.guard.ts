import { inject } from "@angular/core";
import { CanActivateFn, Router } from "@angular/router";
import { map } from "rxjs";
import { PermissionService } from "./permission.service";

// TODO: #4 Allow resource patterns such as role/{id} and replace {id} with _route fragment
export const permissionGuard = (action: string, resource: string): CanActivateFn => {
    return (_route, _state) => {
        const permission = inject(PermissionService);
        const router = inject(Router);
        return permission.check(action, resource).pipe(
            map(isAuthenticated => {
                if (isAuthenticated) {
                    return true;
                } else {
                    return router.createUrlTree(['']);
                }
            })
        );
    };
};