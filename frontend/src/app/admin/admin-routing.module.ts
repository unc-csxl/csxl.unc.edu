import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminComponent } from './admin.component';
import { AdminUsersListComponent } from './users/list/admin-users-list.component';

const routes: Routes = [
  { path: '', component: AdminComponent, children: [
    AdminUsersListComponent.Route,
  ]},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
