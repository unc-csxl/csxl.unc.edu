import { inject } from "@angular/core";
import { CanActivateFn, Router } from "@angular/router";
import { map } from "rxjs";
import { PermissionService } from "./permission.service";

export const permissionGuard = (action: string, resource: string): CanActivateFn => {
    return () => {
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