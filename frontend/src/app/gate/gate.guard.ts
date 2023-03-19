import { inject } from "@angular/core";
import { CanActivateFn, Router } from "@angular/router";
import { map } from "rxjs";
import { AuthenticationService } from "../authentication.service";

export const isAuthenticated: CanActivateFn = (route, state) => {
    const auth = inject(AuthenticationService);
    const router = inject(Router);
    return auth.isAuthenticated$.pipe(
        map(isAuthenticated => {
            if (isAuthenticated) {
                return true;
            } else {
                return router.createUrlTree(['']);
            }
        })
    );
};