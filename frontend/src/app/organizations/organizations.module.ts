import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

/* Angular Material Modules */
import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';

import { OrganizationsPageComponent } from './organizations-page/organizations-page.component';
import { OrganizationsRoutingModule } from './organizations-routing.module';
import { OrgDetailsComponent } from './org-details/org-details.component';

import { OrganizationFilterPipe } from './org-filter/org-filter.pipe';

/* UI Widgets */
import { OrganizationCard } from './widgets/organization-card/organization-card.widget';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { OrgDetailsInfoCard } from './widgets/org-details-info-card/org-details-info-card.widget';

@NgModule({
  declarations: [
    OrganizationsPageComponent,
    OrgDetailsComponent,

    // Pipes
    OrganizationFilterPipe,

    // UI Widgets
    OrganizationCard,
    OrgDetailsInfoCard
  ],
  imports: [
    CommonModule,
    MatTabsModule,
    MatTableModule,
    MatCardModule,
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
    MatIconModule,
    MatTooltipModule,
    OrganizationsRoutingModule,
    RouterModule,
    SharedModule
  ]
})
export class OrganizationsModule { }
