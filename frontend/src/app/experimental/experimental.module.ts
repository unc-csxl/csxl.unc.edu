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

/* UI Widgets */
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { ExperimentalComponent } from './experimental.component';
import { ExperimentalRoutingModule } from './experimental-routing.module';
import { EventCard } from './widgets/event-card/event-card.widget';
import { EventDetailCard } from './widgets/event-detail-card/event-detail-card.widget';
import { EventDetailDialog } from './event-detail-dialog';

@NgModule({
  declarations: [
    ExperimentalComponent,
    EventCard,
    EventDetailCard,
    EventDetailDialog
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
    RouterModule,
    SharedModule,
    ExperimentalRoutingModule
  ]
})
export class ExperimentalModule { }
