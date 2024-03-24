import { Component } from '@angular/core';
import { OfficeHoursService } from '../office-hours.service';
import { FormBuilder } from '@angular/forms';
import { OfficeHoursEventDraft } from '../office-hours.models';

@Component({
  selector: 'app-event-creation-form',
  templateUrl: './event-creation-form.component.html',
  styleUrls: ['./event-creation-form.component.css']
})
export class EventCreationFormComponent {
  public static Route = {
    path: 'spring-2024/comp110/create-new-event',
    title: 'COMP 110: Intro to Programming',
    component: EventCreationFormComponent,
    canActivate: []
  };

  constructor(
    public officeHoursService: OfficeHoursService,
    protected formBuilder: FormBuilder
  ) {}

  public eventForm = this.formBuilder.group({
    event_type: '',
    description: '',
    start_time: '',
    end_time: '',
    location: '',
    location_description: ''
  });

  onSubmit() {
    console.log('got here!');
    //   let event_draft: OfficeHoursEventDraft = {
    //     // TODO: use event form values to set (most of) these
    //     //oh_section: {
    //     // TODO
    //     // id: ,
    //     // title:
    //     //}

    //     // type: OfficeHoursEventType;
    //     description: this.eventForm.value.description ?? '',
    //     location_description: this.eventForm.value.location_description ?? ''
    //     // event_date: Date;
    //     // start_time: Date;
    //     // end_time: Date;
    //   };
    //   this.officeHoursService.createEvent(event_draft).subscribe({
    //     next: (event) => console.log(event) //remove console.log later -> for demo purposes
    //   });
    //   this.eventForm.reset();
    //   // TODO: bring user to a diff location
  }
}
