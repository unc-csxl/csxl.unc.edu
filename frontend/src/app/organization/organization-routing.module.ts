import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OrganizationPageComponent } from './organization-page/organization-page.component';
import { OrganizationDetailsComponent } from './organization-details/organization-details.component';
import { OrganizationEditorComponent } from '/workspace/frontend/src/app/organization/organization-editor/organization-editor.component'

const routes: Routes = [
  OrganizationPageComponent.Route,
  OrganizationDetailsComponent.Route,
  OrganizationEditorComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OrganizationRoutingModule { }

