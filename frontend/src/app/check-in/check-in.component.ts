import { Component } from '@angular/core';

@Component({
  selector: 'app-check-in',
  templateUrl: './check-in.component.html',
})
export class CheckInComponent {
  public static Route = {
    path: 'check-in',
    component: CheckInComponent 
  }
}
