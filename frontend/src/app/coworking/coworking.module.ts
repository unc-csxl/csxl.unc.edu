import { AsyncPipe, CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { CoworkingRoutingModule } from './coworking-routing.module';
import { CoworkingPageComponent } from './coworking-home/coworking-home.component';
import { AmbassadorPageComponent } from './ambassador-home/ambassador-home.component';
import { MatCardModule } from '@angular/material/card';
import { CoworkingReservationCard } from './widgets/coworking-reservation-card/coworking-reservation-card';
import { CoworkingReservationDraft } from './widgets/coworking-reservation-draft/coworking-reservation-draft';
import { MatDividerModule } from '@angular/material/divider';
import { CoworkingDropInCard } from './widgets/dropin-availability-card/dropin-availability-card.widget';
import { MatListModule } from '@angular/material/list';
import { CoworkingHoursCard } from './widgets/operating-hours-panel/operating-hours-panel.widget';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { ReservationComponent } from './reservation/reservation.component';


@NgModule({
  declarations: [
    CoworkingPageComponent,
    ReservationComponent,
    AmbassadorPageComponent,
    CoworkingDropInCard,
    CoworkingReservationCard,
    CoworkingReservationDraft,
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
    MatTableModule,
    AsyncPipe
  ]
})
export class CoworkingModule { }