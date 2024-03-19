import { NgModule } from '@angular/core';
import { OfficeHoursPageComponent } from './office-hours-page/office-hours-page.component';
import { RouterModule, Routes } from '@angular/router';
import { StudentSectionHomeComponent } from './student-section-home/student-section-home.component';

const routes: Routes = [
  OfficeHoursPageComponent.Route,
  StudentSectionHomeComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OfficeHoursRoutingModule {}
