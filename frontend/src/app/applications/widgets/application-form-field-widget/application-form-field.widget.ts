import { Component, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';
import {
  ApplicationFormField,
  FormFieldType
} from '../../form/application-forms';

@Component({
  selector: 'app-application-form-field-widget',
  templateUrl: './application-form-field.widget.html',
  styleUrl: './application-form-field.widget.css'
})
export class ApplicationFormFieldWidget {
  fieldType = FormFieldType;

  @Input() formGroup!: FormGroup;
  @Input() field!: ApplicationFormField;
}
