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
import { TicketCard } from './widgets/ticket-card/ticket-card.widget';
import { TaSectionHomeComponent } from './ta-section-home/ta-section-home.component';
import { CurrentTicketPageComponent } from './current-ticket-page/current-ticket-page.component';
import { CurrentTicketCard } from './widgets/current-ticket-card/current-ticket-card.widget';
import { TicketHistoryWidget } from './widgets/ticket-history/ticket-history.widget';
import { MatTableModule } from '@angular/material/table';
import { InstructorSectionHomeComponent } from './instructor-section-home/instructor-section-home.component';
import { TicketFeedbackFormComponent } from './ticket-feedback-form/ticket-feedback-form.component';
import { TicketFeedbackDialog } from './widgets/ticket-feedback-dialog/ticket-feedback-dialog';

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
    TicketHistoryWidget,
    TicketQueuePageComponent,
    TicketCard,
    TaSectionHomeComponent,
    CurrentTicketPageComponent,
    CurrentTicketCard,
    InstructorSectionHomeComponent,
    TicketFeedbackFormComponent,
    TicketFeedbackDialog
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
    MatMenuModule,
    MatTableModule
  ]
})
export class OfficeHoursModule {}
