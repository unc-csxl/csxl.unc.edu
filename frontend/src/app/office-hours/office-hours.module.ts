import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OfficeHoursPageComponent } from './office-hours-page/office-hours-page.component';
import { OfficeHoursRoutingModule } from './office-hours-routing.module';
import { CreateEventFormComponent } from './event/create-event-form/create-event-form.component';
import { MatButtonModule } from '@angular/material/button';
import { MatTabsModule } from '@angular/material/tabs';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatStepperModule } from '@angular/material/stepper';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatRadioModule } from '@angular/material/radio';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { StudentSectionHomeComponent } from './section/student-section-home/student-section-home.component';
import { EventCard } from './widgets/event/event-card/event-card-widget';
import { ScheduleCard } from './widgets/section/schedule-card/schedule-card-widget';
import { TicketCreationFormComponent } from './ticket/ticket-creation-form/ticket-creation-form.component';
import { MatIconModule } from '@angular/material/icon';
import { CourseCard } from './widgets/section/course-card/course-card-widget';
import { OpenEventHoursCard } from './widgets/event/open-event-hours-card/open-event-hours-card-widget';
import { MatDialogModule } from '@angular/material/dialog';
import { SectionCreationFormComponent } from './section/section-creation-form/section-creation-form.component';
import { MatMenuModule } from '@angular/material/menu';
import { SectionCreationDialog } from './widgets/section/section-creation-dialog/section-creation-dialog.widget';
import { JoinSectionDialog } from './widgets/section/join-section-dialog/join-section-dialog.widget';
import { UpcomingHoursDialog } from './widgets/section/upcoming-hours-dialog/upcoming-hours-dialog.widget';
import { UpcomingHoursText } from './widgets/section/upcoming-hours-text/upcoming-hours-text.widget';
import { TicketQueuePageComponent } from './ticket/ticket-queue-page/ticket-queue-page.component';
import { TicketCard } from './widgets/ticket/ticket-card/ticket-card.widget';
import { TaSectionHomeComponent } from './section/ta-section-home/ta-section-home.component';
import { CurrentTicketPageComponent } from './ticket/current-ticket-page/current-ticket-page.component';
import { CurrentTicketCard } from './widgets/ticket/current-ticket-card/current-ticket-card.widget';
import { TicketHistoryWidget } from './widgets/ticket/ticket-history/ticket-history.widget';
import { MatTableModule } from '@angular/material/table';
import { InstructorSectionHomeComponent } from './section/instructor-section-home/instructor-section-home.component';
import { TicketFeedbackFormComponent } from './ticket/ticket-feedback-form/ticket-feedback-form.component';
import { TicketFeedbackDialog } from './widgets/ticket/ticket-feedback-dialog/ticket-feedback-dialog.widget';
import { PeopleTableComponent } from './section/people-table/people-table.component';
import { DeleteEventFormComponent } from './event/delete-event-form/delete-event-form.component';
import { DeleteEventDialog } from './widgets/event/delete-event-dialog/delete-event-dialog.widget';
import { DeleteTicketDialog } from './widgets/ticket/delete-ticket-dialog/delete-ticket-dialog.widget';
import { SectionData } from './widgets/section/section-data/section-data-widget';
import { ConcernTicketsWidget } from './widgets/ticket/concern-tickets/concern-tickets-widget';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { EditEventFormComponent } from './event/edit-event-form/edit-event-form.component';
import { SharedModule } from '../shared/shared.module';

@NgModule({
  declarations: [
    OfficeHoursPageComponent,
    StudentSectionHomeComponent,
    EventCard,
    ScheduleCard,
    TicketCreationFormComponent,
    CreateEventFormComponent,
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
    TicketFeedbackDialog,
    PeopleTableComponent,
    DeleteEventFormComponent,
    DeleteEventDialog,
    DeleteTicketDialog,
    SectionData,
    ConcernTicketsWidget,
    EditEventFormComponent
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
    MatTableModule,
    MatRadioModule,
    MatCheckboxModule,
    MatButtonToggleModule,
    MatDatepickerModule,
    MatNativeDateModule,
    SharedModule
  ]
})
export class OfficeHoursModule {}
