/**
 * The Signage Module coples all features of the Signage feature into
 * a single unit that can be loaded at once. This decreases load time
 * for the overall application and decouples this feature from other
 * features in the application.
 *
 * @author Andrew Lockard, Will Zahrt
 * @copyright 2024
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

// Angular Material Modules
import { MatCardModule } from '@angular/material/card';
import {
  MatChipAvatar,
  MatChipSet,
  MatChipsModule
} from '@angular/material/chips';
import { MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatTabsModule } from '@angular/material/tabs';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

import { SignageRoutingModule } from './signage-routing.module';
import { SignageComponent } from './signage.component';
import { NewsCardWidget } from './widgets/news-card/news-card.widget';
import { OccupancyWidget } from './widgets/occupancy/occupancy.widget';
import { RoomsWidget } from './widgets/rooms/rooms.widget';
import { SharedModule } from '../shared/shared.module';
import { MatDivider } from '@angular/material/divider';
import { EventCardWidget } from './widgets/event-card/event-card.widget';
import { LeaderboardWidget } from './widgets/leaderboard/leaderboard.widget';
import { OfficeHoursWidget } from './widgets/office-hours/office-hours.widget';
import { PageSpinnerWidget } from './widgets/page-spinner/page-spinner.widget';

@NgModule({
  declarations: [
    SignageComponent,

    // Widgets
    NewsCardWidget,
    OccupancyWidget,
    RoomsWidget,
    EventCardWidget,
    LeaderboardWidget,
    OfficeHoursWidget,
    PageSpinnerWidget
  ],
  imports: [
    SignageRoutingModule,
    CommonModule,
    MatTabsModule,
    MatTableModule,
    MatCardModule,
    MatChipsModule,
    MatDialogModule,
    MatSelectModule,
    MatPaginatorModule,
    MatListModule,
    MatIconModule,
    MatTooltipModule,
    MatSidenavModule,
    MatToolbarModule,
    MatProgressSpinnerModule,
    MatDivider,
    MatChipSet,
    MatChipAvatar,
    RouterModule,
    SharedModule
  ]
})
export class SignageModule {}
