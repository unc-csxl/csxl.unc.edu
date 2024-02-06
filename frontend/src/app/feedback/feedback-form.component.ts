import { Component } from '@angular/core';

@Component({
  selector: 'app-feedback-form',
  templateUrl: './feedback-form.component.html',
  styleUrls: ['./feedback-form.component.css']
})
export class FeedbackFormComponent {
  public static Route = {
    path: 'feedback',
    title: 'Feedback',
    component: FeedbackFormComponent
  };
}
