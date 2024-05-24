/**
 * The Event Module couples all features of the Events feature into a single
 * unit that can be loaded at once. This decreases load time for the overall
 * application and decouples this feature from other features in the application.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
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
import { MatChipsModule } from '@angular/material/chips';

/* UI Widgets */
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { EventRoutingModule } from './event-routing.module';
import { EventDetailCard } from './widgets/event-detail-card/event-detail-card.widget';
import { EventDetailsComponent } from './event-details/event-details.component';
import { EventPageComponent } from './event-page/event-page.component';
import { EventEditorComponent } from './event-editor/event-editor.component';
import { EventUsersList } from './widgets/event-users-list/event-users-list.widget';
import { EventListAdminComponent } from './event-list-admin/event-list-admin.component';
import { GroupEventsPipe } from './pipes/group-events.pipe';

@NgModule({
  declarations: [
    EventDetailCard,
    EventDetailsComponent,
    EventPageComponent,
    EventEditorComponent,
    EventListAdminComponent,
    EventUsersList,
    GroupEventsPipe
  ],
  imports: [
    CommonModule,
    MatTabsModule,
    MatTableModule,
    MatCardModule,
    MatChipsModule,
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
    RouterModule,
    SharedModule,
    EventRoutingModule
  ]
})
export class EventModule {}
