import { Component, inject } from '@angular/core';
import { injectQuery } from '@tanstack/angular-query-experimental';
import { SampleService } from '../sample.service';
import { sample } from 'rxjs';

@Component({
  selector: 'app-sample-page',
  templateUrl: './sample.component.html',
  styleUrls: ['./sample.component.css']
})
export class SamplePageComponent {
  /** Route information to be used in routing module */
  sampleService = inject(SampleService);

  public static Route = {
    path: '',
    title: 'Sample',
    component: SamplePageComponent
  };

  query = this.sampleService.queryGetAll();
}
