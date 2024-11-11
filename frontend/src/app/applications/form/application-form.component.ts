/**
 * The Application Form Component enables students to submit
 * and edit applications.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, WritableSignal, effect, signal } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { ApplicationFormField } from './application-forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ApplicationsService } from '../applications.service';
import { Application, ApplicationSectionChoice } from '../applications.model';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Profile } from 'src/app/models.module';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Term } from 'src/app/academics/academics.models';
import { AcademicsService } from 'src/app/academics/academics.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-application-form',
  templateUrl: './application-form.component.html',
  styleUrl: './application-form.component.css'
})
export class ApplicationFormComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: ':term/:type',
    title: 'Apply',
    component: ApplicationFormComponent,
    resolve: {
      profile: profileResolver
    }
  };

  showApplicationAssignmentCard =
    new Date().getTime() > new Date(2025, 1, 9).getTime();

  /** Form */
  formGroup: FormGroup;
  fields: ApplicationFormField[];
  selectedSections: WritableSignal<ApplicationSectionChoice[]> = signal([]);

  application: Application;

  term$: Observable<Term>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected snackBar: MatSnackBar,
    protected applicationsService: ApplicationsService,
    protected academicsService: AcademicsService
  ) {
    // Load the profile
    const data = this.route.snapshot.data as {
      profile: Profile;
    };
    const profile = data.profile;
    // Load the form
    let type = this.route.snapshot.params['type'];
    [this.formGroup, this.fields] = applicationsService.getForm(type);
    // Load an exising application, if it exists
    let termId = this.route.snapshot.params['term'];
    this.application = {
      id: null,
      user_id: profile.id!,
      term_id: termId,
      type: type,
      academic_hours: null,
      extracurriculars: null,
      expected_graduation: null,
      program_pursued: null,
      other_programs: null,
      gpa: null,
      comp_gpa: null,
      comp_227: null,
      intro_video_url: null,
      prior_experience: null,
      service_experience: null,
      additional_experience: null,
      ta_experience: null,
      best_moment: null,
      desired_improvement: null,
      advisor: null,
      preferred_sections: [],
      assignments: []
    };
    this.applicationsService.getApplication(termId).subscribe((application) => {
      if (application) {
        this.application = application;
        this.formGroup.patchValue(application!);
        this.selectedSections.set(application!.preferred_sections);
      }
    });

    this.term$ = this.academicsService.getTerm(termId);
  }

  onSubmit() {
    if (this.formGroup.valid) {
      let applicationToSubmit = this.application;
      Object.assign(applicationToSubmit, this.formGroup.value);
      applicationToSubmit.preferred_sections = this.selectedSections();

      let result =
        this.application.id == null
          ? this.applicationsService.createApplication(this.application)
          : this.applicationsService.updateApplication(this.application);

      result.subscribe({
        next: (_) => {
          this.router.navigate(['/my-courses/']);
          this.snackBar.open(`Thank you for submitting your application!`, '', {
            duration: 2000
          });
        },
        error: (_) => {
          this.snackBar.open(`Error: Application not submitted.`, '', {
            duration: 2000
          });
        }
      });
    }
  }
}
