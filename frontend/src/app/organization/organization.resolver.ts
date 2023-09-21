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

export const organizationResolver: ResolveFn<Organization | undefined> = (route, state) => {
    return inject(OrganizationService).getOrganization(route.paramMap.get('slug')!);
};