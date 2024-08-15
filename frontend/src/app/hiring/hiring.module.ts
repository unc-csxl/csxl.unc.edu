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
import { HiringPreferencesComponent } from './hiring-preferences/hiring-preferences.component';
import {
  CdkDrag,
  CdkDragPlaceholder,
  CdkDropList
} from '@angular/cdk/drag-drop';
import { ApplicationCardWidget } from './widgets/application-card/application-card.widget';
import { ApplicationDialog } from './dialogs/application-dialog/application-dialog.dialog';
import { YouTubePlayerModule } from '@angular/youtube-player';
import { HiringAdminComponent } from './hiring-admin/hiring-admin.component';
import { CourseHiringCardWidget } from './widgets/course-hiring-card/course-hiring-card.widget';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { LevelsAdminComponent } from './levels-admin/levels-admin.component';
import { LevelEditorComponent } from './levels-admin/level-editor/level-editor.component';
import { MatChipsModule } from '@angular/material/chips';
import { CreateAssignmentDialog } from './dialogs/create-assignment-dialog/create-assignment.dialog';
import { QuickCreateAssignmentDialog } from './dialogs/quick-create-assignment-dialog/quick-create-assignment.dialog';
import { EditAssignmentDialog } from './dialogs/edit-assignment-dialog/edit-assignment.dialog';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { HiringSummaryComponent } from './hiring-summary/hiring-summary.component';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { HiringAssignmentsComponent } from './hiring-assignments/hiring-assignments.component';
import { HiringPageComponent } from './hiring-page/hiring-page.component';

/* UI Widgets */

@NgModule({
  declarations: [
    HiringPreferencesComponent,
    ApplicationCardWidget,
    ApplicationDialog,
    HiringAdminComponent,
    CourseHiringCardWidget,
    LevelsAdminComponent,
    LevelEditorComponent,
    CreateAssignmentDialog,
    QuickCreateAssignmentDialog,
    EditAssignmentDialog,
    HiringSummaryComponent,
    HiringAssignmentsComponent,
    HiringPageComponent
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
    HiringRoutingModule,
    RouterModule,
    SharedModule,
    CdkDrag,
    CdkDropList,
    CdkDragPlaceholder,
    YouTubePlayerModule,
    MatButtonToggleModule,
    MatChipsModule,
    MatSlideToggleModule,
    MatCheckboxModule
  ]
})
export class HiringModule {}
