import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OfficeHoursPageComponent } from './office-hours-page/office-hours-page.component';
import { OfficeHoursRoutingModule } from './office-hours-routing.module';
import { StudentSectionHomeComponent } from './student-section-home/student-section-home.component';

@NgModule({
  declarations: [OfficeHoursPageComponent, StudentSectionHomeComponent],
  imports: [CommonModule, OfficeHoursRoutingModule]
})
export class OfficeHoursModule {}
