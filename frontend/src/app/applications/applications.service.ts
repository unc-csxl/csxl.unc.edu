/**
 * The Applications Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Injectable } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { GTA_APPLICATION_FORM } from './form/application-forms';

@Injectable({
  providedIn: 'root'
})
export class ApplicationsService {
  /**
   * Generates an application form based on the type of application.
   * @param type: Type of application ('uta' | 'gta')
   * @returns: Form group for the application
   */
  getFormGroup(type: string): FormGroup {
    let formGroup = new FormGroup({});
    if (type == 'gta') {
      for (let field of GTA_APPLICATION_FORM) {
        formGroup.addControl(
          field.name,
          new FormControl('', field.required ? [Validators.required] : [])
        );
      }
    }
    return formGroup;
  }
}
