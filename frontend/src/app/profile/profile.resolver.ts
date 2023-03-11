import { inject } from "@angular/core";
import { ResolveFn } from "@angular/router";
import { Profile, ProfileService } from "./profile.service";

export const profileResolver: ResolveFn<Profile | undefined> = (route, state) => {
    return inject(ProfileService).profile$;
};