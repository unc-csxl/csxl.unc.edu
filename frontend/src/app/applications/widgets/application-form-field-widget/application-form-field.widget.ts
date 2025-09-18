import { Component, Input, WritableSignal, signal } from '@angular/core';
import {
  ControlContainer,
  FormGroup,
  FormGroupDirective
} from '@angular/forms';
import {
  ApplicationFormField,
  FormFieldType
} from '../../form/application-forms';
import { ApplicationsService } from '../../applications.service';
import { ApplicationSectionChoice } from '../../applications.model';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';

@Component({
    selector: 'application-form-field',
    templateUrl: './application-form-field.widget.html',
    styleUrl: './application-form-field.widget.css',
    viewProviders: [
        {
            provide: ControlContainer,
            useExisting: FormGroupDirective
        }
    ],
    standalone: false
})
export class ApplicationFormFieldWidget {
  fieldType = FormFieldType;

  @Input() field!: ApplicationFormField;
  @Input() selectedSections: WritableSignal<ApplicationSectionChoice[]> =
    signal([]);
  currentSectionInput = signal('');

  constructor(protected applicationsService: ApplicationsService) {}

  /**
   * Handles the selection of items from the autocomplete dropdown for sections.
   *
   * Logic from the dialog example on the Angular Material docs:
   * https://material.angular.io/components/chips/examples#chips-autocomplete
   */
  selectedSection(event: MatAutocompleteSelectedEvent): void {
    let section = event.option.value as ApplicationSectionChoice;
    this.selectedSections.update((sections) => [...sections, section]);
    this.currentSectionInput.set('');
    event.option.deselect();
  }

  /**
   * Handles the removal of items from the autocomplete dropdown for sections.
   *
   * Logic from the dialog example on the Angular Material docs:
   * https://material.angular.io/components/chips/examples#chips-autocomplete
   */
  removeSection(setion: ApplicationSectionChoice): void {
    this.selectedSections.update((sections) => {
      let index = sections.indexOf(setion);
      if (index < 0) {
        return sections;
      }

      sections.splice(index, 1);
      return [...sections];
    });
  }
}
