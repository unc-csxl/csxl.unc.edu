import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OfficeHoursPageComponent } from './office-hours-page/office-hours-page.component';
import { OfficeHoursRoutingModule } from './office-hours-routing.module';
import { StudentSectionHomeComponent } from './student-section-home/student-section-home.component';
import { EventCard } from './widgets/event-card/event-card-widget';
import { MatButtonModule } from '@angular/material/button';
import { MatTabsModule } from '@angular/material/tabs';
import { ScheduleCard } from './widgets/schedule-card/schedule-card-widget';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { TicketCreationFormComponent } from './ticket-creation-form/ticket-creation-form.component';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatStepperModule } from '@angular/material/stepper';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { CourseCard } from './widgets/course-card/course-card-widget';
import { OpenEventHoursCard } from './widgets/open-event-hours-card/open-event-hours-card-widget';
import { MatDialogModule } from '@angular/material/dialog';
import { SectionCreationFormComponent } from './section-creation-form/section-creation-form.component';
import { MatMenuModule } from '@angular/material/menu';

@NgModule({
  declarations: [
    OfficeHoursPageComponent,
    StudentSectionHomeComponent,
    EventCard,
    ScheduleCard,
    TicketCreationFormComponent,
    CourseCard,
    OpenEventHoursCard,
    SectionCreationFormComponent
  ],
  imports: [
    CommonModule,
    OfficeHoursRoutingModule,
    MatButtonModule,
    MatTabsModule,
    MatCardModule,
    MatDividerModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatStepperModule,
    ReactiveFormsModule,
    FormsModule,
    MatInputModule,
    MatIconModule,
    MatDialogModule,
    MatMenuModule
  ]
})
export class OfficeHoursModule {}
