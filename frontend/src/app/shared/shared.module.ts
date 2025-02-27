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
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';

/* UI Widgets */
import { SocialMediaIcon } from '../shared/social-media-icon/social-media-icon.widget';
import { SearchBar } from './search-bar/search-bar.widget';
import { RouterModule } from '@angular/router';
import { UserLookup } from './user-lookup/user-lookup.widget';
import { CommunityAgreement } from './community-agreement/community-agreement.widget';

import { UserChipList } from './user-chip-list/user-chip-list.widget';
import { MatPaneComponent } from './mat/mat-pane/mat-pane.component';
import { BannerCardComponent } from './banner-card/banner-card.component';
import { GroupEventsPipe } from '../event/pipes/group-events.pipe';
import { AdminFabComponent } from './admin-fab/admin-fab.component';
import { TabContainerWidget } from './tab-container/tab-container.widget';

import { YouTubePlayer } from '@angular/youtube-player';
import {
  CoworkingHoursCard,
  OperatingHoursCapitalizationPipe
} from './operating-hours-panel/operating-hours-panel.widget';
import { MarkdownDirective } from './directives/markdown.directive';
import { EventRegistrationCardWidget } from './event-registration-card/event-registration-card.widget';
import { AboutPaneWidget } from './about-pane/about-pane.widget';
import { MatFilterChipComponent } from './mat/filter-chip/filter-chip.component';
import { MatFilterChipDialog } from './mat/filter-chip/dialog/filter-chip-dialog.component';

@NgModule({
  declarations: [
    SocialMediaIcon,
    SearchBar,
    UserLookup,
    UserChipList,
    CommunityAgreement,
    MatPaneComponent,
    BannerCardComponent,
    AdminFabComponent,
    TabContainerWidget,
    CoworkingHoursCard,
    OperatingHoursCapitalizationPipe,
    MarkdownDirective,
    EventRegistrationCardWidget,
    AboutPaneWidget,
    MatFilterChipComponent,
    MatFilterChipDialog
  ],
  imports: [
    CommonModule,
    MatTabsModule,
    MatChipsModule,
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
    MatCheckboxModule,
    FormsModule,
    ReactiveFormsModule,
    MatIconModule,
    MatTooltipModule,
    MatSlideToggleModule,
    RouterModule,
    YouTubePlayer
  ],
  exports: [
    SocialMediaIcon,
    SearchBar,
    UserLookup,
    UserChipList,
    MatPaneComponent,
    BannerCardComponent,
    AdminFabComponent,
    TabContainerWidget,
    CoworkingHoursCard,
    MarkdownDirective,
    EventRegistrationCardWidget,
    AboutPaneWidget,
    MatFilterChipComponent
  ],
  providers: [GroupEventsPipe]
})
export class SharedModule {}
