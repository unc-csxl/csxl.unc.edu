import { Component, OnInit } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Router
} from '@angular/router';
import { ohSectionResolver } from '../../office-hours.resolver';
import { OfficeHoursService } from '../../office-hours.service';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators
} from '@angular/forms';
import { AcademicsService } from 'src/app/academics/academics.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import {
  OfficeHoursEvent,
  OfficeHoursEventDetails,
  OfficeHoursEventDraft,
  OfficeHoursEventModeType,
  OfficeHoursEventPartial,
  OfficeHoursEventType,
  OfficeHoursSectionDetails
} from '../../office-hours.models';
import { Room, RosterRole } from 'src/app/academics/academics.models';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['section']?.title ?? 'Section Not Found';
};

@Component({
  selector: 'app-edit-event-form',
  templateUrl: './edit-event-form.component.html',
  styleUrls: ['./edit-event-form.component.css']
})
export class EditEventFormComponent implements OnInit {
  public static Routes = [
    {
      path: 'ta/:id/edit-event/:eventId',
      component: EditEventFormComponent,
      canActivate: [],
      resolve: { section: ohSectionResolver },
      children: [
        {
          path: '',
          title: titleResolver,
          component: EditEventFormComponent
        }
      ]
    },
    {
      path: 'instructor/:id/edit-event/:eventId',
      component: EditEventFormComponent,
      canActivate: [],
      resolve: { section: ohSectionResolver },
      children: [
        {
          path: '',
          title: titleResolver,
          component: EditEventFormComponent
        }
      ]
    }
  ];

  /* List of available rooms to hold Office Hours event */
  rooms: Room[] = [];

  /* Section that the Office Hours event is being held for */
  sectionId: number;
  section: OfficeHoursSectionDetails | undefined;

  /* Event ID */
  eventId: string = 'upcoming';
  event: OfficeHoursEventDetails | undefined;

  /* Upcoming event list */
  events: OfficeHoursEvent[] = [];

  isUpcoming: boolean = false;

  // RosterRole to determine if user can view this routed component
  rosterRole: RosterRole | undefined;
  eventForm: FormGroup = this.formBuilder.group({
    event_title: [''],
    event_type: ['', Validators.required],
    event_mode: ['', Validators.required],
    description: '',
    event_date: ['', Validators.required],
    start_time: ['', Validators.required],
    end_time: ['', Validators.required],
    location: ['', Validators.required],
    location_description: ''
  });

  /* Holds Information About Virtual Room */
  virtualRoom: Room | undefined;

  /* Section that the Office Hours event is being held for */
  isVirtualOurLink: boolean = false;

  constructor(
    public officeHoursService: OfficeHoursService,
    protected formBuilder: FormBuilder,
    public academicsService: AcademicsService,
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar,
    private router: Router,
    private activatedRoute: ActivatedRoute
  ) {
    this.sectionId = this.route.snapshot.params['id'];
    this.getRosterRole();
  }

  /* Get rooms and associated section upon initialization */
  ngOnInit() {
    this.getRooms();
    this.getSection();
    this.eventId = this.route.snapshot.params['eventId'];
    if (this.eventId === 'upcoming') {
      this.isUpcoming = true;
    }

    this.getEventDetails();

    // Prevent Chrome From Crashing In Form Dropdown
    document.addEventListener('DOMNodeInserted', function () {
      const elements = document.querySelectorAll('[aria-owns]');

      elements.forEach((element) => {
        element.removeAttribute('aria-owns');
      });
    });
  }

  /* EventForm contains data pertaining to event that is being created/modified */
  getRosterRole() {
    this.academicsService
      .getMembershipBySection(this.sectionId)
      .subscribe((role) => (this.rosterRole = role.member_role));
  }

  /* Get list of available Rooms to hold office hours event in */
  getRooms() {
    this.academicsService.getRooms().subscribe((rooms) => {
      this.rooms = rooms;
      this.virtualRoom = rooms.find((room) => room.id === 'Virtual');
    });
  }

  /* Get room that has been selected from list of options */
  getSelectedRoom(): Room | undefined {
    return this.rooms.find((room) => room.id === this.eventForm.value.location);
  }

  /* Gets OfficeHoursSection that event belongs to */
  getSection() {
    this.officeHoursService.getSection(this.sectionId).subscribe((section) => {
      this.section = section;
      this.getUpcomingEvents();
    });
  }

  /* Gets all upcoming events for the Office Hours Section */
  getUpcomingEvents() {
    this.officeHoursService
      .getAllUpcomingEventsBySection(this.sectionId)
      .subscribe((events) => {
        this.events = events;
      });
  }

  /* Get OfficeHoursEventDetails for selected event and populate form with its data */
  getEventDetails() {
    if (this.eventId !== 'upcoming') {
      let eventIdNum = Number(this.eventId);
      this.officeHoursService.getEvent(eventIdNum).subscribe((event) => {
        this.event = event;

        this.eventForm.setValue({
          event_title: event.id,
          event_type: this.reverseMapEventType(event.type),
          event_mode: this.reverseMapEventMode(event.mode),
          description: event.description,
          event_date: event.event_date,
          start_time: event.start_time.split('T')[1],
          end_time: event.end_time.split('T')[1],
          location: event.room.id,
          location_description: event.location_description
        });
      });
    }
  }

  // Handles Room Location Value According to Event Mode Selection Changes
  onEventModeChange(event: any) {
    // CASE: If Event Mode is Virtual, Will Set Default Room Location to Virtual
    if (event.value.includes('virtual')) {
      if (this.virtualRoom) {
        (this.eventForm.get('location') as FormControl).setValue(
          this.virtualRoom.id
        );
      }
      // CASE: If Location has been selected but switch to In-Person, will reset selection for Room Location
    } else if (
      event.value.includes('in_person') &&
      this.eventForm.value.location !== ''
    ) {
      (this.eventForm.get('location') as FormControl).setValue(null);
    }

    this.isVirtualOurLink = event.value.includes('our_link');
  }

  /* On changing selected event, re-populate form with newly selected data */
  onEventChange(event: any) {
    this.eventId = event.value;
    this.getEventDetails();
  }

  onSubmit() {
    // Logic for assigning the correct OfficeHoursEventType and OfficeHoursEventMode enum
    let event_type: OfficeHoursEventType = this.mapEventType(
      this.eventForm.value.event_type
    );

    let event_mode: OfficeHoursEventModeType = this.mapEventMode(
      this.eventForm.value.event_mode
    );

    // Ensure start and end times aren't none
    if (!this.eventForm.value.start_time) {
      this.eventForm.value.start_time = '';
    }
    if (!this.eventForm.value.end_time) {
      this.eventForm.value.end_time = '';
    }

    // Ensure that section must not be null to create/edit event
    if (this.section) {
      var event_draft: OfficeHoursEventPartial = {
        id: this.event?.id ?? -1,
        oh_section: this.section,
        room: this.getSelectedRoom() ?? null,
        type: event_type,
        mode: event_mode,
        description: this.eventForm.value.description ?? '',
        location_description: this.eventForm.value.location_description ?? '',
        event_date: this.eventForm.value.event_date,
        start_time:
          this.eventForm.value.event_date +
          'T' +
          this.eventForm.value.start_time,
        end_time:
          this.eventForm.value.event_date + 'T' + this.eventForm.value.end_time
      };

      this.officeHoursService.updateEvent(event_draft).subscribe({
        next: () => this.onSuccess(),
        error: (err) => this.onError(err)
      });
    }
  }

  /* Maps event type string to OfficeHoursEventType enum */
  private mapEventType(eventType: string): OfficeHoursEventType {
    switch (eventType) {
      case 'office_hours':
        return OfficeHoursEventType.OFFICE_HOURS;
      case 'tutoring':
        return OfficeHoursEventType.TUTORING;
      case 'review_session':
        return OfficeHoursEventType.REVIEW_SESSION;
      default:
        return OfficeHoursEventType.OFFICE_HOURS;
    }
  }

  /* Maps OfficeHoursEventType enum to string */
  private reverseMapEventType(eventType: OfficeHoursEventType): string {
    switch (eventType) {
      case OfficeHoursEventType.OFFICE_HOURS:
        return 'office_hours';
      case OfficeHoursEventType.TUTORING:
        return 'tutoring';
      case OfficeHoursEventType.REVIEW_SESSION:
        return 'review_session';
      default:
        return 'office_hours';
    }
  }

  /* Maps event mode string to OfficeHoursEventModeType enum */
  private mapEventMode(eventMode: string): OfficeHoursEventModeType {
    switch (eventMode) {
      case 'in_person':
        return OfficeHoursEventModeType.IN_PERSON;
      case 'virtual_our_link':
        return OfficeHoursEventModeType.VIRTUAL_OUR_LINK;
      case 'virtual_student_link':
        return OfficeHoursEventModeType.VIRTUAL_STUDENT_LINK;
      default:
        return OfficeHoursEventModeType.IN_PERSON;
    }
  }

  /* Maps OfficeHoursEventModeType enum to string */
  private reverseMapEventMode(eventMode: OfficeHoursEventModeType): string {
    switch (eventMode) {
      case OfficeHoursEventModeType.IN_PERSON:
        return 'in_person';
      case OfficeHoursEventModeType.VIRTUAL_OUR_LINK:
        return 'virtual_our_link';
      case OfficeHoursEventModeType.VIRTUAL_STUDENT_LINK:
        return 'virtual_student_link';
      default:
        return 'in_person';
    }
  }

  /* On successful event creation, navigate back to section home */
  private onSuccess(): void {
    this.snackBar.open('You have updated your event!', '', {
      duration: 3000
    });
    this.router.navigate(['../../'], { relativeTo: this.activatedRoute });
    this.eventForm.reset();
  }

  /* On error, display message informing user */
  private onError(err: any): void {
    this.snackBar.open('Error: Unable to update event', '', {
      duration: 2000
    });
    console.log(err.description);
  }

  /* Helper function to format event type */
  public formatEventType(type: OfficeHoursEventType) {
    return this.officeHoursService.formatEventType(type);
  }
}
