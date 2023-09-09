import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { CoworkingRoutingModule } from './coworking-routing.module';
import { CoworkingPageComponent } from './coworking-page/coworking-page.component';
import { AmbassadorPageComponent } from './ambassador-page/ambassador-page.component';
import { MatCardModule } from '@angular/material/card';
import { CoworkingReservationCard } from './widgets/coworking-reservation-card/coworking-reservation-card';
import { CoworkingReservationEditor } from './widgets/coworking-reservation-editor/coworking-reservation-editor';
import { MatDividerModule } from '@angular/material/divider';
import { CoworkingDropInCard } from './widgets/coworking-dropin-card/coworking-dropin-card.widget';
import { MatListModule } from '@angular/material/list';
import { CoworkingHoursCard } from './widgets/coworking-hours-card/coworking-hours-card.widget';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';


@NgModule({
  declarations: [
    CoworkingPageComponent,
    AmbassadorPageComponent,
    CoworkingDropInCard,
    CoworkingReservationCard,
    CoworkingReservationEditor,
    CoworkingHoursCard,
  ],
  imports: [
    CommonModule,
    CoworkingRoutingModule,
    MatCardModule,
    MatDividerModule,
    MatListModule,
    MatExpansionModule,
    MatButtonModule,
    MatTableModule
  ]
})
export class CoworkingModule { }