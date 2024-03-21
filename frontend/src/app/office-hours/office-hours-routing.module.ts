import { NgModule } from '@angular/core';
import { OfficeHoursPageComponent } from './office-hours-page/office-hours-page.component';
import { RouterModule, Routes } from '@angular/router';
import { EventCreationFormComponent } from './event-creation-form/event-creation-form.component';

const routes: Routes = [
  OfficeHoursPageComponent.Route,
  EventCreationFormComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OfficeHoursRoutingModule {}
