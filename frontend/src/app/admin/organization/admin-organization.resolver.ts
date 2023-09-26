/**
 * The Admin Organization Resolver allows the organizations to be injected into the routes
 * of components.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { inject } from "@angular/core";
import { ResolveFn } from "@angular/router";
import { Organization } from "/workspace/frontend/src/app/organization/organization.service";
import { AdminOrganizationService } from "./admin-organization.service"

export const adminOrganizationResolver: ResolveFn<Organization[] | undefined> = (route, state) => {
    return inject(AdminOrganizationService).list();
};