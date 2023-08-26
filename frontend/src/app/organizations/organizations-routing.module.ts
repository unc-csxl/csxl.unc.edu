import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OrganizationsPageComponent } from './organizations-page/organizations-page.component';
import { OrgDetailsComponent } from './org-details/org-details.component';

const routes: Routes = [
  OrganizationsPageComponent.Route,
  OrgDetailsComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OrganizationsRoutingModule { }

