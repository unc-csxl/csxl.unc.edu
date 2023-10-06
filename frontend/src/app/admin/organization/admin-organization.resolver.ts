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
import { Organizations } from "/workspace/frontend/src/app/organization/organization.service";
import { AdminOrganizationService } from "./admin-organization.service"

export const adminOrganizationResolver: ResolveFn<Organizations | undefined> = (route, state) => {
    let service = inject(AdminOrganizationService);
    service.list();
    return service.organizations$;
};