import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OfficeHoursPageComponent } from './office-hours-page/office-hours-page.component';
import { OfficeHoursRoutingModule } from './office-hours-routing.module';
import { EventCreationFormComponent } from './event-creation-form/event-creation-form.component';
import { MatButtonModule } from '@angular/material/button';
import { MatTabsModule } from '@angular/material/tabs';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatStepperModule } from '@angular/material/stepper';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { StudentSectionHomeComponent } from './student-section-home/student-section-home.component';
import { EventCard } from './widgets/event-card/event-card-widget';
import { ScheduleCard } from './widgets/schedule-card/schedule-card-widget';
import { TicketCreationFormComponent } from './ticket-creation-form/ticket-creation-form.component';
import { MatIconModule } from '@angular/material/icon';
import { CourseCard } from './widgets/course-card/course-card-widget';
import { OpenEventHoursCard } from './widgets/open-event-hours-card/open-event-hours-card-widget';
import { MatDialogModule } from '@angular/material/dialog';
import { SectionCreationFormComponent } from './section-creation-form/section-creation-form.component';
import { MatMenuModule } from '@angular/material/menu';
import { SectionCreationDialog } from './widgets/section-creation-dialog/section-creation-dialog.widget';
import { JoinSectionDialog } from './widgets/join-section-dialog/join-section-dialog.widget';
import { UpcomingHoursDialog } from './widgets/upcoming-hours-dialog/upcoming-hours-dialog.widget';
import { UpcomingHoursText } from './widgets/upcoming-hours-text/upcoming-hours-text.widget';
import { TicketQueuePageComponent } from './ticket-queue-page/ticket-queue-page.component';

@NgModule({
  declarations: [
    OfficeHoursPageComponent,
    StudentSectionHomeComponent,
    EventCard,
    ScheduleCard,
    TicketCreationFormComponent,
    EventCreationFormComponent,
    CourseCard,
    SectionCreationDialog,
    OpenEventHoursCard,
    SectionCreationFormComponent,
    JoinSectionDialog,
    UpcomingHoursDialog,
    UpcomingHoursText,
    TicketQueuePageComponent
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
