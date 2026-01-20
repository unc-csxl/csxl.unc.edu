import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
    selector: 'app-hiring-page',
    templateUrl: './hiring-page.component.html',
    styleUrl: './hiring-page.component.css',
    standalone: false
})
export class HiringPageComponent {
  links = [
    {
      label: 'Preferences',
      path: `/hiring/${this.route.snapshot.params['courseSiteId']}/preferences`,
      icon: 'format_list_numbered'
    },
    {
      label: 'Assignments',
      path: `/hiring/${this.route.snapshot.params['courseSiteId']}/assignments`,
      icon: 'assignment'
    }
  ];

  constructor(private route: ActivatedRoute) {}
}
