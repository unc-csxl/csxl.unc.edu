import { inject } from "@angular/core";
import { ResolveFn } from "@angular/router";
import { ProfileService } from "./profile.service";
import { Profile } from "../models.module";

export const profileResolver: ResolveFn<Profile | undefined> = (route, state) => {
    return inject(ProfileService).profile$;
};