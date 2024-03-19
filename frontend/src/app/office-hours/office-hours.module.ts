import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OfficeHoursPageComponent } from './office-hours-page/office-hours-page.component';
import { OfficeHoursRoutingModule } from './office-hours-routing.module';
import { StudentSectionHomeComponent } from './student-section-home/student-section-home.component';
import { EventCard } from './widgets/event-card/event-card-widget';
import { MatButton, MatButtonModule } from '@angular/material/button';
import { MatTabsModule } from '@angular/material/tabs';
import { ScheduleCard } from './widgets/schedule-card/schedule-card-widget';
import { MatCardModule } from '@angular/material/card';
import { MatDivider, MatDividerModule } from '@angular/material/divider';
import { TicketCreationFormComponent } from './ticket-creation-form/ticket-creation-form.component';
import { MatFormField, MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatStepperModule } from '@angular/material/stepper';

@NgModule({
  declarations: [OfficeHoursPageComponent, StudentSectionHomeComponent, EventCard, ScheduleCard, TicketCreationFormComponent],
  imports: [
    CommonModule,
    OfficeHoursRoutingModule,
    MatButtonModule,
    MatTabsModule,
    MatCardModule,
    MatDividerModule,
    MatFormFieldModule,
    FormsModule,
    ReactiveFormsModule,
    MatStepperModule,
  ]
})
export class OfficeHoursModule {}
