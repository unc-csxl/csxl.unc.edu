import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';

interface Experience {
  value: string;
  viewValue: string;
}

@Component({
  selector: 'uta-application',
  templateUrl: 'uta-application.component.html',
  styleUrls: ['uta-application.component.css']
})
export class UndergradApplicationComponent {
  public static Route = {
    path: 'uta-application',
    component: UndergradApplicationComponent
  };
  experienceList: Experience[] = [
    { value: 'none-0', viewValue: 'No Prior programming experience' },
    {
      value: 'few-1',
      viewValue:
        'I followed a few self-paced courses but did not invest a lot of time'
    },
    {
      value: 'self-taught-2',
      viewValue: 'I was self-taught and invested a lot of time'
    },
    {
      value: 'ap-3',
      viewValue: 'I took AP Computer Science or some other CS courses in HS'
    }
  ];

  firstFormGroup = this._formBuilder.group({
    firstCtrl: ['', Validators.required]
  });
  secondFormGroup = this._formBuilder.group({
    secondCtrl: ['', Validators.required]
  });
  thirdFormGroup = this._formBuilder.group({
    thirdCtrl: ['', Validators.required]
  });
  fourthFormGroup = this._formBuilder.group({
    fourthCtrl: ['', Validators.required]
  });
  fifthFormGroup = this._formBuilder.group({
    fifthCtrl: ['', Validators.required]
  });
  isLinear = false;

  constructor(private _formBuilder: FormBuilder) {}
}
