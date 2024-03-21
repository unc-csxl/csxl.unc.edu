import { Component } from '@angular/core';

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
}
