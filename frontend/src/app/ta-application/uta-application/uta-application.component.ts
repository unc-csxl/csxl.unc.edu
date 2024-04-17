import { Component, OnDestroy, OnInit } from '@angular/core';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import {
  FormArray,
  FormBuilder,
  FormControl,
  FormGroup,
  Validators
} from '@angular/forms';
import { Application } from 'src/app/admin/applications/admin-application.model';
import { ApplicationsService } from '../ta-application.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import {
  Observable,
  Subject,
  filter,
  map,
  startWith,
  switchMap,
  take,
  takeUntil
} from 'rxjs';
import { MatChipInputEvent } from '@angular/material/chips';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { Section } from 'src/app/academics/academics.models';
import { Profile } from 'src/app/profile/profile.service';

interface OptionSelect {
  value: string;
  viewValue: string;
}

@Component({
  selector: 'uta-application',
  templateUrl: 'uta-application.component.html',
  styleUrls: ['uta-application.component.css']
})
export class UndergradApplicationComponent implements OnInit, OnDestroy {
  public static Route = {
    path: 'uta-application',
    component: UndergradApplicationComponent
  };

  experienceList: OptionSelect[] = [
    {
      value: 'No Prior programming experience',
      viewValue: 'No Prior programming experience'
    },
    {
      value:
        'I followed a few self-paced courses but did not invest a lot of time',
      viewValue:
        'I followed a few self-paced courses but did not invest a lot of time'
    },
    {
      value: 'I was self-taught and invested a lot of time',
      viewValue: 'I was self-taught and invested a lot of time'
    },
    {
      value: 'I took AP Computer Science or some other CS courses in HS',
      viewValue: 'I took AP Computer Science or some other CS courses in HS'
    }
  ];

  expectedGraduationDates: OptionSelect[] = [
    { value: '2024 - Fall', viewValue: '2024 - Fall' },
    {
      value: '2025 - Spring',
      viewValue: '2025 - Spring'
    },
    {
      value: '2025 - Fall',
      viewValue: '2025 - Fall'
    },
    {
      value: '2026 - Spring',
      viewValue: '2026 - Spring'
    },
    {
      value: '2026 - Fall',
      viewValue: '2026 - Fall'
    },
    {
      value: '2027 - Spring',
      viewValue: '2027 - Spring'
    },
    {
      value: '2027 - Fall',
      viewValue: '2027 - Fall'
    }
  ];

  programsList: OptionSelect[] = [
    { value: 'CS Minor', viewValue: 'CS Minor' },
    {
      value: 'CS Major (BS)',
      viewValue: 'CS Major (BS)'
    },
    {
      value: 'CS Major (BA)',
      viewValue: 'CS Major (BA)'
    },
    {
      value: 'None of the above',
      viewValue: 'None of the above'
    }
  ];

  comp227: OptionSelect[] = [
    {
      value: 'Monetary compensation only',
      viewValue: 'Monetary compensation only'
    },
    {
      value: 'COMP 227 credit only',
      viewValue: 'COMP 227 credit only'
    },
    {
      value: 'Open to either 227 credit or compensation',
      viewValue: 'Open to either 227 credit or compensation'
    }
  ];

  validateIntroVideo(control: FormControl): { [key: string]: any } | null {
    const valid = control.value && control.value.includes('youtu');
    return valid ? null : { invalidURL: true };
  }

  firstFormGroup: FormGroup;
  secondFormGroup: FormGroup;
  thirdFormGroup: FormGroup;
  fourthFormGroup: FormGroup;
  fifthFormGroup: FormGroup;

  isLinear = false;
  userId!: number | null;

  separatorKeysCodes: number[] = [ENTER, COMMA];
  preferenceCtrl = new FormControl('');
  filteredPreferences: Observable<Section[]>;
  allSections$: Observable<Section[]>;
  selectedSections: Section[] = [];
  userDetails: Profile | null = null;
  private destroy$ = new Subject<void>();

  constructor(
    private formBuilder: FormBuilder,
    private applicationService: ApplicationsService,
    private router: Router,
    protected snackBar: MatSnackBar
  ) {
    this.firstFormGroup = this.formBuilder.group({
      intro_video: [
        '',
        [Validators.required, this.validateIntroVideo.bind(this)]
      ]
    });
    this.secondFormGroup = this.formBuilder.group({
      prior_experience: ['', Validators.required],
      service_experience: ['', Validators.required],
      additional_experience: ['', Validators.required]
    });
    this.thirdFormGroup = this.formBuilder.group({
      academic_hours: [0, [Validators.required, Validators.min(0)]],
      extracurriculars: ['', Validators.required],
      expected_graduation: ['', Validators.required],
      program_pursued: ['', Validators.required],
      other_programs: ['']
    });
    this.fourthFormGroup = this.formBuilder.group({
      gpa: [0.0, [Validators.required, Validators.min(0)]],
      comp_gpa: [0.0, [Validators.required, Validators.min(0)]]
    });
    this.fifthFormGroup = this.formBuilder.group({
      preferred_sections: this.formBuilder.array([]),
      comp_227: ['', Validators.required]
    });

    this.allSections$ = applicationService.sections$;
    applicationService.getSections();

    this.filteredPreferences = this.preferenceCtrl.valueChanges.pipe(
      startWith(''),
      switchMap((value) => this.filterSections(value || ''))
    );

    this.applicationService.user_application$.subscribe((application) => {
      if (application) {
        this.populateForm(application);
      }
    });
  }

  ngOnInit(): void {
    this.applicationService.getApplication().subscribe(
      (response) => {
        const application = response ? response['application'] : null;
        if (application) {
          this.populateForm(application);
        } else {
          this.resetForm();
        }
      },
      (error) => {
        console.error('Failed to fetch application:', error);
        this.snackBar.open('Failed to fetch application details!', 'Close', {
          duration: 3000
        });
      }
    );
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

  setPreferredSections(sections: Section[]): void {
    const sectionFormGroups = sections.map((section) => {
      return new FormGroup({
        id: new FormControl(section.id),
        course_id: new FormControl(section.course_id),
        number: new FormControl(section.number),
        term_id: new FormControl(section.term_id),
        meeting_pattern: new FormControl(section.meeting_pattern),
        lecture_room: new FormGroup({
          id: new FormControl(section.lecture_room?.id || ''),
          nickname: new FormControl(section.lecture_room?.nickname || '')
        }),
        staff: new FormArray(
          (section.staff || []).map(
            (staffMember) =>
              new FormGroup({
                id: new FormControl(staffMember.id),
                first_name: new FormControl(staffMember.first_name),
                last_name: new FormControl(staffMember.last_name),
                member_role: new FormControl(staffMember.member_role),
                pronouns: new FormControl(staffMember.pronouns)
              })
          )
        ),
        office_hour_rooms: new FormArray(
          (section.office_hour_rooms || []).map(
            (room) =>
              new FormGroup({
                id: new FormControl(room.id),
                nickname: new FormControl(room.nickname)
              })
          )
        ),
        override_title: new FormControl(section.override_title),
        override_description: new FormControl(section.override_description)
      });
    });

    this.fifthFormGroup.setControl(
      'preferred_sections',
      new FormArray(sectionFormGroups)
    );
  }

  populateForm(application: Application | null): void {
    if (application) {
      this.firstFormGroup.patchValue({
        intro_video: application.intro_video
      });
      this.secondFormGroup.patchValue({
        prior_experience: application.prior_experience,
        service_experience: application.service_experience,
        additional_experience: application.additional_experience
      });
      this.thirdFormGroup.patchValue({
        academic_hours: application.academic_hours,
        extracurriculars: application.extracurriculars,
        expected_graduation: application.expected_graduation,
        program_pursued: application.program_pursued,
        other_programs: application.other_programs
      });
      this.fourthFormGroup.patchValue({
        gpa: application.gpa,
        comp_gpa: application.comp_gpa
      });
      this.fifthFormGroup.patchValue({
        comp_227: application.comp_227
      });

      this.setPreferredSections(application.preferred_sections || []);
      this.selectedSections = application.preferred_sections || [];
    } else {
      this.resetForm();
    }
  }

  private validateForm(): boolean {
    return (
      this.firstFormGroup.valid &&
      this.secondFormGroup.valid &&
      this.thirdFormGroup.valid &&
      this.fourthFormGroup.valid &&
      this.fifthFormGroup.valid
    );
  }

  private collectFormData(userDetails: Profile): Omit<Application, 'id'> {
    const sectionsToSend = this.selectedSections.map((section) => ({
      id: section.id,
      course_id: section.course_id,
      number: section.number,
      term_id: section.term_id,
      meeting_pattern: section.meeting_pattern,
      lecture_room: section.lecture_room ?? { id: '', nickname: '' },
      staff: section.staff ?? [],
      office_hour_rooms: section.office_hour_rooms ?? [],
      override_title: section.override_title || '',
      override_description: section.override_description || ''
    }));

    return {
      user_id: userDetails.id ?? 1,
      user: userDetails,
      academic_hours: this.thirdFormGroup.value.academic_hours ?? 0,
      extracurriculars: this.thirdFormGroup.value.extracurriculars ?? '',
      expected_graduation: this.thirdFormGroup.value.expected_graduation ?? '',
      program_pursued: this.thirdFormGroup.value.program_pursued ?? '',
      other_programs: this.thirdFormGroup.value.other_programs ?? '',
      gpa: this.fourthFormGroup.value.gpa ?? 0.0,
      comp_gpa: this.fourthFormGroup.value.comp_gpa ?? 0.0,
      preferred_sections: sectionsToSend,
      comp_227: this.fifthFormGroup.value.comp_227 ?? '',
      intro_video: this.firstFormGroup.value.intro_video ?? '',
      prior_experience: this.secondFormGroup.value.prior_experience ?? '',
      service_experience: this.secondFormGroup.value.service_experience ?? '',
      additional_experience:
        this.secondFormGroup.value.additional_experience ?? ''
    } as Omit<Application, 'id'>;
  }

  resetForm(): void {
    this.firstFormGroup.reset();
    this.secondFormGroup.reset();
    this.thirdFormGroup.reset();
    this.fourthFormGroup.reset();
    this.fifthFormGroup.reset();
  }

  onSubmit(): void {
    if (this.validateForm()) {
      this.applicationService.getProfile().subscribe({
        next: (userDetails) => {
          const formData = this.collectFormData(userDetails);
          this.applicationService.submitApplication(formData).subscribe({
            next: (application) => this.onSuccess(application),
            error: (err) => this.onError(err)
          });
        },
        error: (err) => {
          console.error('Failed to fetch user details:', err);
          this.snackBar.open('Failed to fetch user details.', '', {
            duration: 3000
          });
        }
      });
    } else {
      this.snackBar.open('Please complete all required fields.', '', {
        duration: 3000
      });
    }
  }

  filterSections(value: string): Observable<Section[]> {
    const filterValue = value.toLowerCase();
    return this.applicationService.sections$.pipe(
      map((sections) =>
        sections.filter(
          (section) =>
            section.course?.subject_code.toLowerCase().includes(filterValue)
        )
      )
    );
  }

  addPreferences(event: MatChipInputEvent): void {
    const input = event.input;
    const value = event.value;

    if ((value || '').trim()) {
      const sectionId = Number(value.trim());

      this.applicationService.sections$
        .pipe(
          map((sections) =>
            sections.find((section) => section.id === sectionId)
          ),
          take(1)
        )
        .subscribe((section) => {
          if (section && !this.selectedSections.includes(section)) {
            this.selectedSections.push(section);
          }
        });
    }

    if (input) {
      input.value = '';
    }

    this.preferenceCtrl.setValue(null);
  }

  selectedPreferences(event: MatAutocompleteSelectedEvent): void {
    const section: Section = event.option.value;
    if (
      !this.selectedSections.some(
        (selectedSection) => selectedSection.id === section.id
      )
    ) {
      this.selectedSections.push(section);
    }
    this.preferenceCtrl.setValue(null);
  }

  removeSection(index: number): void {
    const sectionsArray = this.fifthFormGroup.get(
      'preferred_sections'
    ) as FormArray;
    if (sectionsArray) {
      sectionsArray.removeAt(index);
      this.selectedSections.splice(index, 1); // Keep the array and form sync
    }
  }

  getInstructorName(section: Section): string {
    if (section.staff && section.staff.length > 0 && section.staff[0]) {
      const instructor = section.staff[0];
      return `${instructor.first_name} ${instructor.last_name}`;
    } else {
      return 'Instructor TBA';
    }
  }

  capitalizedCourseId(section: Section): string {
    return section.course_id.toUpperCase();
  }

  fetchUserProfile() {
    this.applicationService.getProfile().subscribe({
      next: (userDetails) => {
        this.userId = userDetails.id;
      },
      error: (err) => {
        console.error('Failed to fetch user details', err);
      }
    });
  }

  /** Opens a confirmation snackbar when an application is successfully submitted.
   * @returns {void}
   */
  private onSuccess(application: Application): void {
    this.router.navigate(['/ta-application/']);
    this.snackBar.open('Application Submitted!', '', { duration: 2000 });
  }

  /** Opens a snackbar when there is an error submitting an application.
   * @returns {void}
   */
  private onError(err: any): void {
    console.error('Error processing the application:', err);
    this.snackBar.open(
      'Error processing your application. Please try again.',
      '',
      { duration: 3000 }
    );
  }
}
