import { Component } from '@angular/core';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html'
})
export class AboutComponent {
  public static Route = {
    path: 'about',
    component: AboutComponent
  }
}
