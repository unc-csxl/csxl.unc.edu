/**
 * The Prfoile Module couples all features of the Profile Page feature
 * into a single unit that can be loaded at once. This decreases load time
 * for the overall application and decouples this feature from other features
 * in the application.
 *
 * @author Jade Keegan
 * @copyright 2023
 * @license MIT
 */

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
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { ProfilePageComponent } from './profile-page/profile-page.component';
import { ProfileEditorComponent } from './profile-editor/profile-editor.component';
import { ProfileRoutingModule } from './profile-routing.module';
import { MatChipsModule } from '@angular/material/chips';
import { PublicProfilePageComponent } from './public-profile-page/public-profile-page.component';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';

@NgModule({
  declarations: [
    ProfilePageComponent,
    ProfileEditorComponent,
    PublicProfilePageComponent
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
    ProfileRoutingModule,
    RouterModule,
    SharedModule,
    MatChipsModule,
    MatSlideToggleModule,
  ]
})
export class ProfileModule {}
