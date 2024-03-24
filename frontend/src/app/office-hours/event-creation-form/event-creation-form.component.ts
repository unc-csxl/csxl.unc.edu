import { Component } from '@angular/core';
import { OfficeHoursService } from '../office-hours.service';
import { FormBuilder } from '@angular/forms';

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

  onSubmit() {}
}
