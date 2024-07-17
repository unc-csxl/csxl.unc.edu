/**
 * The Applications Module couples all features of the applications feature
 * into a single unit that can be loaded at once. This decreases load time
 * for the overall application and decouples this feature from other features.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatDialogModule } from '@angular/material/dialog';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatChipsModule } from '@angular/material/chips';
import { MatInputModule } from '@angular/material/input';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { ApplicationsRoutingModule } from './applications-routing.module';
import { ApplicationFormComponent } from './form/application-form.component';
import { ApplicationFormFieldWidget } from './widgets/application-form-field-widget/application-form-field.widget';

@NgModule({
  declarations: [ApplicationFormComponent, ApplicationFormFieldWidget],
  imports: [
    CommonModule,
    ApplicationsRoutingModule,
    RouterModule,
    SharedModule,
    MatCardModule,
    MatDividerModule,
    MatButtonModule,
    MatIconModule,
    MatTabsModule,
    MatTableModule,
    MatFormFieldModule,
    MatSelectModule,
    FormsModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatPaginatorModule,
    MatButtonToggleModule,
    MatChipsModule,
    MatInputModule,
    MatAutocompleteModule
  ]
})
export class ApplicationsModule {}
