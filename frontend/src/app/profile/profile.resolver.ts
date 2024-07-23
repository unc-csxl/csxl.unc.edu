import { inject } from '@angular/core';
import { ResolveFn, Router } from '@angular/router';
import { Profile, ProfileService, PublicProfile } from './profile.service';
import { tap } from 'rxjs';

export const profileResolver: ResolveFn<Profile | undefined> = (
  route,
  state
) => {
  return inject(ProfileService).profile$;
};

export const publicProfileResolver: ResolveFn<PublicProfile> = (
  route,
  state
) => {
  let profileService = inject(ProfileService);
  let router = inject(Router);
  return profileService.getByOnyen(route.params['onyen']).pipe(
    tap((profile) => {
      if (profile.onyen == profileService.profile()?.onyen) {
        router.navigateByUrl('/profile');
      }
    })
  );
};
