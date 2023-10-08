/**
 * The Organization Resolver allows the organization to be injected into the routes
 * of components.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { inject } from "@angular/core";
import { ResolveFn } from "@angular/router";
import { Organization, OrganizationService } from "./organization.service"

export const organizationResolver: ResolveFn<Organization[] | undefined> = (route, state) => {
    return inject(OrganizationService).getOrganizations();
};

export const organizationDetailResolver: ResolveFn<Organization | undefined> = (route, state) => {
    if(route.paramMap.get('slug')! != "new") {
        return inject(OrganizationService).getOrganization(route.paramMap.get('slug')!);
    }
    else {
        return {
            id: null,
            name: "",
            shorthand: "",
            slug: "",
            logo: "",
            short_description: "",
            long_description: "",
            email: "",
            website: "",
            instagram: "",
            linked_in: "",
            youtube: "",
            heel_life: "",
            public: false
          };
    }
};