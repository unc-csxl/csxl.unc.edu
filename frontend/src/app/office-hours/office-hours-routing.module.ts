import { NgModule } from '@angular/core';
import { OfficeHoursPageComponent } from './office-hours-page/office-hours-page.component';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [OfficeHoursPageComponent.Route];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OfficeHoursRoutingModule {}
