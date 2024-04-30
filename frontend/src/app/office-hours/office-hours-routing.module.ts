import { NgModule } from '@angular/core';
import { OfficeHoursPageComponent } from './office-hours-page/office-hours-page.component';
import { RouterModule, Routes } from '@angular/router';
import { CreateEventFormComponent } from './event/create-event-form/create-event-form.component';
import { StudentSectionHomeComponent } from './section/student-section-home/student-section-home.component';
import { TicketCreationFormComponent } from './ticket/ticket-creation-form/ticket-creation-form.component';
import { TicketQueuePageComponent } from './ticket/ticket-queue-page/ticket-queue-page.component';
import { TaSectionHomeComponent } from './section/ta-section-home/ta-section-home.component';
import { CurrentTicketPageComponent } from './ticket/current-ticket-page/current-ticket-page.component';
import { InstructorSectionHomeComponent } from './section/instructor-section-home/instructor-section-home.component';
import { EditEventFormComponent } from './event/edit-event-form/edit-event-form.component';

const routes: Routes = [
  OfficeHoursPageComponent.Route,
  CreateEventFormComponent.Routes[0],
  CreateEventFormComponent.Routes[1],
  StudentSectionHomeComponent.Route,
  TicketCreationFormComponent.Route,
  TicketQueuePageComponent.Routes[0],
  TicketQueuePageComponent.Routes[1],
  TaSectionHomeComponent.Route,
  CurrentTicketPageComponent.Route,
  InstructorSectionHomeComponent.Route,
  EditEventFormComponent.Routes[0],
  EditEventFormComponent.Routes[1]
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OfficeHoursRoutingModule {}
