import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { Profile, ProfileService, PublicProfile } from './profile.service';

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
  return inject(ProfileService).getByOnyen(route.params['onyen']);
};
