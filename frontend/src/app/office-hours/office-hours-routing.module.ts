import { NgModule } from '@angular/core';
import { OfficeHoursPageComponent } from './office-hours-page/office-hours-page.component';
import { RouterModule, Routes } from '@angular/router';
import { EventCreationFormComponent } from './event-creation-form/event-creation-form.component';
import { StudentSectionHomeComponent } from './student-section-home/student-section-home.component';
import { TicketCreationFormComponent } from './ticket-creation-form/ticket-creation-form.component';
import { TicketQueuePageComponent } from './ticket-queue-page/ticket-queue-page.component';
import { TaSectionHomeComponent } from './ta-section-home/ta-section-home.component';
import { CurrentTicketPageComponent } from './current-ticket-page/current-ticket-page.component';
import { InstructorSectionHomeComponent } from './instructor-section-home/instructor-section-home.component';

const routes: Routes = [
  OfficeHoursPageComponent.Route,
  EventCreationFormComponent.Routes[0],
  EventCreationFormComponent.Routes[1],
  StudentSectionHomeComponent.Route,
  TicketCreationFormComponent.Route,
  TicketQueuePageComponent.Routes[0],
  TicketQueuePageComponent.Routes[1],
  TaSectionHomeComponent.Route,
  CurrentTicketPageComponent.Route,
  InstructorSectionHomeComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OfficeHoursRoutingModule {}
