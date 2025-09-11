import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CoworkingPageComponent } from './coworking-home/coworking-home.component';
import { ReservationComponent } from './reservation/reservation.component';
import { NewRoomReservationComponent } from './room-reservation/room-reservation.component';
import { OperatingHoursComponent } from './operating-hours/operating-hours.component';
import { OperatingHoursEditorComponent } from './operating-hours/editor/operating-hours-editor.component';

const routes: Routes = [
  CoworkingPageComponent.Route,
  ReservationComponent.Route,
  NewRoomReservationComponent.Route,
  OperatingHoursComponent.Route,
  OperatingHoursEditorComponent.Route,
  {
    path: 'ambassador',
    title: 'Ambassador',
    loadChildren: () =>
      import('./ambassador-home/ambassador-home.module').then(
        (m) => m.AmbassadorHomeModule
      )
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CoworkingRoutingModule {}
