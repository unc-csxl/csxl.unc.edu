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

import { OrganizationPageComponent } from './organization-page/organization-page.component';
import { OrganizationRoutingModule } from './organization-routing.module';
import { OrganizationDetailsComponent } from './organization-details/organization-details.component';

import { OrganizationFilterPipe } from './organization-filter/organization-filter.pipe';

/* UI Widgets */
import { OrganizationCard } from './widgets/organization-card/organization-card.widget';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { OrganizationDetailsInfoCard } from './widgets/organization-details-info-card/organization-details-info-card.widget';

@NgModule({
  declarations: [
    OrganizationPageComponent,
    OrganizationDetailsComponent,

    // Pipes
    OrganizationFilterPipe,

    // UI Widgets
    OrganizationCard,
    OrganizationDetailsInfoCard
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
    OrganizationRoutingModule,
    RouterModule,
    SharedModule
  ]
})
export class OrganizationModule { }
