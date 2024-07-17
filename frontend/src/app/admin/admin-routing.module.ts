import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminUsersRolesComponent } from './users-and-roles/admin-users-roles.component';
import { AdminRoleDetailsComponent } from './users-and-roles/roles/details/admin-role-details.component';
import { AdminRolesListComponent } from './users-and-roles/roles/list/admin-roles-list.component';
import { AdminUsersListComponent } from './users-and-roles/users/admin-users.component';
import { AdminComponent } from './admin.component';

const routes: Routes = [
  {
    path: '',
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
