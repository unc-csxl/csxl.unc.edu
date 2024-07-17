import { Component } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { ApplicationFormField } from './application-forms';
import { ActivatedRoute } from '@angular/router';
import { ApplicationsService } from '../applications.service';

@Component({
  selector: 'app-application-form',
  templateUrl: './application-form.component.html',
  styleUrl: './application-form.component.css'
})
export class ApplicationFormComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: ':type',
    title: 'Apply',
    component: ApplicationFormComponent,
    canActivate: []
  };

  /** Form */
  formGroup: FormGroup;
  fields: ApplicationFormField[];

  constructor(
    private route: ActivatedRoute,
    protected applicationssService: ApplicationsService
  ) {
    let type = this.route.snapshot.params['type'];
    [this.formGroup, this.fields] = applicationssService.getForm(type);

    console.log(this.formGroup);
    console.log(this.fields);
  }
}
