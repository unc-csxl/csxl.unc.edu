import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OrganizationsPageComponent } from './organizations-page/organizations-page.component';

const routes: Routes = [
  { path: '', component: OrganizationsPageComponent, children: [
    //AdminUsersListComponent.Route,
    //AdminRolesListComponent.Route,
    //AdminRoleDetailsComponent.Route,
  ]},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OrganizationsRoutingModule { }

