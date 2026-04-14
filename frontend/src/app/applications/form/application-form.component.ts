/**
 * The Application Form Component enables students to submit
 * and edit applications.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  DestroyRef,
  WritableSignal,
  inject,
  signal
} from '@angular/core';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import { FormGroup } from '@angular/forms';
import { ApplicationFormField } from './application-forms';
import { ActivatedRoute, Data, ParamMap, Router } from '@angular/router';
import { ApplicationsService } from '../applications.service';
import { Application, ApplicationSectionChoice } from '../applications.model';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Profile } from 'src/app/models.module';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Term } from 'src/app/academics/academics.models';
import { AcademicsService } from 'src/app/academics/academics.service';
import { Observable, combineLatest, concat, of, timer } from 'rxjs';
import {
  distinctUntilChanged,
  map,
  shareReplay,
  switchMap
} from 'rxjs/operators';

@Component({
  selector: 'app-application-form',
  templateUrl: './application-form.component.html',
  standalone: false
})
export class ApplicationFormComponent {
  private readonly destroyRef = inject(DestroyRef);

  /** Route information to be used in the routing module */
  public static Route = {
    path: ':term/:type',
    title: 'Apply',
    component: ApplicationFormComponent,
    resolve: {
      profile: profileResolver
    }
  };

  /** Form */
  formGroup!: FormGroup;
  fields!: ApplicationFormField[];
  selectedSections: WritableSignal<ApplicationSectionChoice[]> = signal([]);

  application!: Application;

  term$: Observable<Term>;
  showApplicationAssignmentCard$: Observable<boolean>;
  term = toSignal<Term | undefined>(of(undefined));
  showApplicationAssignmentCard = toSignal(of(false), {
    initialValue: false
  });

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected snackBar: MatSnackBar,
    protected applicationsService: ApplicationsService,
    protected academicsService: AcademicsService
  ) {
    const termId$ = this.route.paramMap.pipe(
      map((params: ParamMap) => params.get('term') ?? ''),
      distinctUntilChanged()
    );
    const type$ = this.route.paramMap.pipe(
      map((params: ParamMap) => params.get('type') ?? ''),
      distinctUntilChanged()
    );
    const profile$ = this.route.data.pipe(
      map((data: Data) => (data as { profile: Profile }).profile)
    );

    combineLatest([termId$, type$, profile$])
      .pipe(
        switchMap(([termId, type, profile]: [string, string, Profile]) => {
          [this.formGroup, this.fields] =
            this.applicationsService.getForm(type);
          this.application = this.buildEmptyApplication(profile, termId, type);
          this.formGroup.reset(this.application);
          this.selectedSections.set([]);

          return this.applicationsService.getApplication(termId).pipe(
            map((application: Application | null) => ({
              application:
                application ?? this.buildEmptyApplication(profile, termId, type)
            }))
          );
        }),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe(({ application }: { application: Application }) => {
        this.application = application;
        this.formGroup.reset(application);
        this.selectedSections.set(application.preferred_sections);
      });

    this.term$ = termId$.pipe(
      switchMap((termId: string) => this.academicsService.getTerm(termId)),
      shareReplay({ bufferSize: 1, refCount: true })
    );
    this.showApplicationAssignmentCard$ = this.term$.pipe(
      switchMap((term: Term) => this.watchApplicationAssignmentCard(term))
    );
    this.term = toSignal(this.term$);
    this.showApplicationAssignmentCard = toSignal(
      this.showApplicationAssignmentCard$,
      { initialValue: false }
    );
  }

  private buildEmptyApplication(
    profile: Profile,
    termId: string,
    type: string
  ): Application {
    return {
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
  }

  private shouldShowApplicationAssignmentCard(term: Term): boolean {
    const now = Date.now();
    const termStart = new Date(term.start).getTime();

    if (Number.isNaN(termStart)) {
      return false;
    }

    const applicationsOpen = new Date(term.applications_open).getTime();
    const applicationsClose = new Date(term.applications_close).getTime();
    const applicationWindowIsOpen =
      !Number.isNaN(applicationsOpen) &&
      !Number.isNaN(applicationsClose) &&
      applicationsOpen <= now &&
      now <= applicationsClose;

    if (applicationWindowIsOpen) {
      return false;
    }

    return now >= termStart;
  }

  private watchApplicationAssignmentCard(term: Term): Observable<boolean> {
    const shouldShowAssignmentCard =
      this.shouldShowApplicationAssignmentCard(term);
    const nextTransitionDelay = this.getNextAssignmentCardTransitionDelay(term);

    if (nextTransitionDelay === null) {
      return of(shouldShowAssignmentCard);
    }

    return concat(
      of(shouldShowAssignmentCard),
      timer(nextTransitionDelay).pipe(
        switchMap(() => this.watchApplicationAssignmentCard(term))
      )
    );
  }

  private getNextAssignmentCardTransitionDelay(term: Term): number | null {
    const now = Date.now();
    const transitionTimes = [
      new Date(term.applications_open).getTime(),
      new Date(term.applications_close).getTime(),
      new Date(term.start).getTime()
    ].filter((time): time is number => !Number.isNaN(time) && time > now);

    if (transitionTimes.length === 0) {
      return null;
    }

    return Math.max(Math.min(...transitionTimes) - now, 1);
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
        next: (_: Application) => {
          this.router.navigate(['/my-courses/']);
          this.snackBar.open(`Thank you for submitting your application!`, '', {
            duration: 2000
          });
        },
        error: (_: unknown) => {
          this.snackBar.open(`Error: Application not submitted.`, '', {
            duration: 2000
          });
        }
      });
    }
  }
}
