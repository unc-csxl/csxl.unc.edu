import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminUsersRolesComponent } from './accounts/admin-accounts.component';
import { AdminRoleDetailsComponent } from './accounts/roles/details/admin-role-details.component';
import { AdminRolesListComponent } from './accounts/roles/list/admin-roles-list.component';
import { AdminUsersListComponent } from './accounts/users/admin-users.component';
import { AdminComponent } from './admin.component';

const routes: Routes = [
  {
    path: '',
    title: 'Site Administration',
    component: AdminComponent
  },
  {
    path: 'accounts',
    component: AdminUsersRolesComponent,
    children: [
      AdminUsersListComponent.Route,
      AdminRolesListComponent.Route,
      AdminRoleDetailsComponent.Route
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule {}
