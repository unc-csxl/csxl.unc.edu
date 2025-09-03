import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CoworkingPageComponent } from './coworking-home/coworking-home.component';
import { ReservationComponent } from './reservation/reservation.component';
import { NewReservationPageComponent } from './room-reservation/new-reservation-page/new-reservation-page.component';
import { ConfirmReservationComponent } from './room-reservation/confirm-reservation/confirm-reservation.component';
import { CoworkingAdminComponent } from './coworking-admin/coworking-admin.component';

const routes: Routes = [
  CoworkingPageComponent.Route,
  ReservationComponent.Route,
  NewReservationPageComponent.Route,
  ConfirmReservationComponent.Route,
  {
    path: 'ambassador',
    title: 'Ambassador',
    loadChildren: () =>
      import('./ambassador-home/ambassador-home.module').then(
        (m) => m.AmbassadorHomeModule
      )
  },
  CoworkingAdminComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CoworkingRoutingModule {}
