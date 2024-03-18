import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OfficeHoursPageComponent } from './office-hours-page/office-hours-page.component';
import { OfficeHoursRoutingModule } from './office-hours-routing.module';

@NgModule({
  declarations: [OfficeHoursPageComponent],
  imports: [CommonModule, OfficeHoursRoutingModule]
})
export class OfficeHoursModule {}
