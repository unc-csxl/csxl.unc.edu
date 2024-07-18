/**
 * The Applications Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Injectable, WritableSignal, signal } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import {
  ApplicationFormField,
  FormFieldType,
  GTA_APPLICATION_FORM
} from './form/application-forms';
import { HttpClient } from '@angular/common/http';
import { Application, ApplicationSectionChoice } from './applications.model';
import { Observable, map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApplicationsService {
  /** Signal to store the sections that a student can rank their preference for.*/
  private eligibleSectionsSignal: WritableSignal<ApplicationSectionChoice[]> =
    signal([]);
  eligibleSections = this.eligibleSectionsSignal.asReadonly();

  /** Constructor */
  constructor(protected http: HttpClient) {
    this.getEligibleSections();
  }

  /**
   * Get the application for the user based on a given term.
   * @param termId: Term ID to get an application of
   * @returns the user's application
   */
  getApplication(termId: string): Observable<Application | null> {
    return this.http.get<Application | null>(
      `/api/applications/ta/user/${termId}`
    );
  }

  /** Creates an application and returns the result. */
  createApplication(application: Application): Observable<Application> {
    return this.http.post<Application>(`/api/applications/ta`, application);
  }

  /** Updates an application and returns the result. */
  updateApplication(application: Application): Observable<Application> {
    return this.http.put<Application>(`/api/applications/ta`, application);
  }

  /**
   * Retrieves the list of eligible sections that a student can apply to for the
   * active application period.
   */
  getEligibleSections() {
    this.http
      .get<ApplicationSectionChoice[]>('/api/applications/ta/eligible-sections')
      .subscribe((sections) => {
        this.eligibleSectionsSignal.set(sections);
      });
  }

  /**
   * Generates an application form based on the type of application.
   * @param type: Type of application ('uta' | 'gta')
   * @returns: Tuple in form (group, fields)
   */
  getForm(type: string): [FormGroup, ApplicationFormField[]] {
    let formGroup = new FormGroup({});
    let fields: ApplicationFormField[] = [];
    if (type == 'gta') {
      for (let field of GTA_APPLICATION_FORM) {
        if (field.fieldType != FormFieldType.COURSE_PREFERENCE) {
          formGroup.addControl(
            field.name,
            new FormControl('', field.required ? [Validators.required] : [])
          );
        }
      }
      fields = GTA_APPLICATION_FORM;
    }
    return [formGroup, fields];
  }
}
