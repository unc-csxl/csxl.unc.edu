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
import { SocialMediaIcon } from '../shared/social-media-icon/social-media-icon.widget';
import { SearchBar } from './search-bar/search-bar.widget';
import { EventCard } from './event-card/event-card.widget';
import { RouterModule } from '@angular/router';
import { EventList } from './event-list/event-list.widget';
import { EventFilterPipe } from '../event/event-filter/event-filter.pipe';

@NgModule({
  declarations: [SocialMediaIcon, SearchBar, EventCard, EventList],
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
    RouterModule
  ],
  exports: [SocialMediaIcon, SearchBar, EventCard, EventList]
})
export class SharedModule {}
