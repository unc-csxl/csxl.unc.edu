import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CoworkingPageComponent } from './coworking-home/coworking-home.component';
import { AmbassadorPageComponent } from './ambassador-home/ambassador-home.component';
import { ReservationComponent } from './reservation/reservation.component';
import { NewReservationPageComponent } from './room-reservation/new-reservation-page/new-reservation-page.component';
import { ConfirmReservationComponent } from './room-reservation/confirm-reservation/confirm-reservation.component';
import { AmbassadorXlListComponent } from './ambassador-home/ambassador-xl/list/ambassador-xl-list.component';

const routes: Routes = [
  CoworkingPageComponent.Route,
  ReservationComponent.Route,
  AmbassadorXlListComponent.Route,
  NewReservationPageComponent.Route,
  ConfirmReservationComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CoworkingRoutingModule {}
