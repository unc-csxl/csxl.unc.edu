/**
 * The Organization Routing Module holds all of the routes that are children
 * to the path /organizations/...
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OrganizationPageComponent } from './organization-page/organization-page.component';
import { OrganizationDetailsComponent } from './organization-details/organization-details.component';
import { OrganizationEditorComponent } from './organization-editor/organization-editor.component';
import { OrganizationListAdminComponent } from './organization-admin/list/organization-list-admin.component';

const routes: Routes = [
  OrganizationPageComponent.Route,
  OrganizationDetailsComponent.Route,
  OrganizationEditorComponent.Route,
  OrganizationListAdminComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OrganizationRoutingModule {}
