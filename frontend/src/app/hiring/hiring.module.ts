/**
 * The Hiring Module couples all features for hiring TAs for
 * computer science courses.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
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
import { HiringRoutingModule } from './hiring-routing.module';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { HiringPageComponent } from './hiring-page/hiring-page.component';
import {
  CdkDrag,
  CdkDragPlaceholder,
  CdkDropList
} from '@angular/cdk/drag-drop';
import { ApplicationCardWidget } from './widgets/application-card/application-card.widget';
import { ApplicationDialog } from './dialogs/application-dialog/application-dialog.dialog';
import { YouTubePlayerModule } from '@angular/youtube-player';

/* UI Widgets */

@NgModule({
  declarations: [HiringPageComponent, ApplicationCardWidget, ApplicationDialog],
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
    HiringRoutingModule,
    RouterModule,
    SharedModule,
    CdkDrag,
    CdkDropList,
    CdkDragPlaceholder,
    YouTubePlayerModule
  ]
})
export class HiringModule {}
