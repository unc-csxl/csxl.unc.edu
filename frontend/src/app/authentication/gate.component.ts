/**
 * Redirect the user to the correct place upon authentication. If the user is authenticated, but has
 * not registered, we take them to the registration page. Otherwise, we attempt to take them to the
 * URL they were accessing when required to authenticated. Otherwise, we redirect them home.
 * 
 * @author Kris Jordan
 * @copyright 2023
 * @license MIT
 */

import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Profile } from '../profile/profile.service';

@Component({ template: '' })
export class GateComponent {

    constructor(private route: ActivatedRoute, private router: Router) {
        const profile = route.snapshot.data['profile'] as Profile | undefined;

        if (profile === undefined) {
            this.router.navigate(['']);
            return;
        }

        let queryParams = this.route.snapshot.queryParams as { continue_to?: string };

        if (profile && profile.registered) {
            if (queryParams.continue_to) {
                let pathParts = queryParams.continue_to.split('/').filter(s => s != '');
                if (pathParts.length > 0) {
                    console.log(pathParts);
                    this.router.navigate(pathParts);
                    return;
                }
            }
            this.router.navigate(['']);
        } else {
            this.router.navigate(['profile'], { queryParams });
        }
    }

}