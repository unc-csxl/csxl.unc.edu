import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { MatTableModule } from '@angular/material/table';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { AdminRoutingModule } from './admin-routing.module';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '../shared/shared.module';
import { MatCardModule } from '@angular/material/card';
import { AdminComponent } from './admin.component';
import { AdminUsersRolesComponent } from './users-and-roles/admin-users-roles.component';
import { AdminUsersListComponent } from './users-and-roles/users/admin-users.component';
import { AdminRolesListComponent } from './users-and-roles/roles/list/admin-roles-list.component';
import { AdminRoleDetailsComponent } from './users-and-roles/roles/details/admin-role-details.component';

@NgModule({
  declarations: [
    AdminComponent,
    AdminUsersRolesComponent,
    AdminUsersListComponent,
    AdminRolesListComponent,
    AdminRoleDetailsComponent
  ],
  imports: [
    CommonModule,
    AdminRoutingModule,
    MatTabsModule,
    MatTableModule,
    MatDialogModule,
    MatButtonModule,
    MatSelectModule,
    MatFormFieldModule,
    MatInputModule,
    MatPaginatorModule,
    MatListModule,
    MatAutocompleteModule,
    FormsModule,
    ReactiveFormsModule,
    SharedModule,
    MatCardModule
  ]
})
export class AdminModule {}
