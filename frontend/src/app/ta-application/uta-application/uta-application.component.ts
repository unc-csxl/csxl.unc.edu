import { Component, ElementRef, ViewChild } from '@angular/core';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { Application } from 'src/app/admin/applications/admin-application.model';
import { ApplicationsService } from '../ta-application.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, filter, map, startWith, switchMap, take } from 'rxjs';
import { MatChipInputEvent } from '@angular/material/chips';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { Course, Section } from 'src/app/academics/academics.models';

interface OptionSelect {
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

  openPairing: OptionSelect[] = [
    { value: 'Yes', viewValue: 'Yes' },
    {
      value: 'No',
      viewValue: 'No'
    }
  ];

  firstFormGroup = this.formBuilder.group({
    intro_video: ['', Validators.required]
  });
  secondFormGroup = this.formBuilder.group({
    prior_experience: ['', Validators.required],
    service_experience: ['', Validators.required],
    additional_experience: ['', Validators.required]
  });
  thirdFormGroup = this.formBuilder.group({
    academic_hours: [null, [Validators.required, Validators.min(0)]],
    extracurriculars: ['', Validators.required],
    expected_graduation: ['', Validators.required],
    program_pursued: ['', Validators.required],
    other_programs: ['']
  });
  fourthFormGroup = this.formBuilder.group({
    gpa: ['', Validators.required],
    comp_gpa: ['', Validators.required]
  });
  fifthFormGroup = this.formBuilder.group({
    preferred_courses: this.formBuilder.array([]),
    eligible_courses: this.formBuilder.array([]),
    comp_227: ['', Validators.required],
    open_pairing: ['', Validators.required]
  });

  isLinear = false;
  userId!: number | null;

  separatorKeysCodes: number[] = [ENTER, COMMA];
  preferenceCtrl = new FormControl('');
  filteredPreferences: Observable<Section[]>;
  allSections$: Observable<Section[]>;
  selectedSections: Section[] = [];

  // @ViewChild('fruitInput') fruitInput: ElementRef<HTMLInputElement> | undefined;

  constructor(
    private formBuilder: FormBuilder,
    private applicationService: ApplicationsService,
    private router: Router,
    protected snackBar: MatSnackBar
  ) {
    this.allSections$ = applicationService.sections$;
    applicationService.getSections();

    this.filteredPreferences = this.preferenceCtrl.valueChanges.pipe(
      startWith(''),
      switchMap((value) => this.filterSections(value!))
    );
  }

  private filterSections(value: string): Observable<Section[]> {
    const filterValue = value.toLowerCase();
    return this.allSections$.pipe(
      map((sections) =>
        sections.filter(
          (section) =>
            section.course?.subject_code.toLowerCase().includes(filterValue)
        )
      )
    );
  }

  addPreferences(event: MatChipInputEvent): void {
    const input = event.chipInput;
    let value = event.value;

    if (value) {
      value = value.trim();
      const sectionId = Number(value);

      this.allSections$
        .pipe(
          map((sections) =>
            sections.find((section) => section.id === sectionId)
          ),
          filter((section) => !!section),
          take(1)
        )
        .subscribe((section) => {
          if (
            section &&
            !this.selectedSections.some(
              (selected) => selected.id === section.id
            )
          ) {
            this.selectedSections.push(section);
          }
        });
    }

    input?.clear();
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

  removeSection(sectionID: number | null): void {
    const index = this.selectedSections.findIndex(
      (section) => section.id === sectionID
    );
    if (index >= 0) {
      this.selectedSections.splice(index, 1);
    }
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

  onSubmit() {
    if (
      this.firstFormGroup.valid &&
      this.secondFormGroup.valid &&
      this.thirdFormGroup.valid &&
      this.fourthFormGroup.valid &&
      this.fifthFormGroup.valid
    ) {
      this.applicationService.getProfile().subscribe({
        next: (userDetails) => {
          const formData: Omit<Application, 'id'> = {
            user_id: userDetails.id ?? 0,
            user: userDetails,
            academic_hours: this.thirdFormGroup.value.academic_hours ?? 0,
            extracurriculars: this.thirdFormGroup.value.extracurriculars ?? '',
            expected_graduation:
              this.thirdFormGroup.value.expected_graduation ?? '',
            program_pursued: this.thirdFormGroup.value.program_pursued ?? '',
            other_programs: this.thirdFormGroup.value.other_programs ?? '',
            gpa: this.fourthFormGroup.value.gpa ?? '',
            comp_gpa: this.fourthFormGroup.value.comp_gpa ?? '',
            preferred_courses: this.fifthFormGroup.value.preferred_courses,
            eligible_courses: this.fifthFormGroup.value.eligible_courses,
            comp_227: this.fifthFormGroup.value.comp_227 ?? '',
            open_pairing:
              this.fifthFormGroup.value.open_pairing === 'Yes' ||
              this.fifthFormGroup.value.open_pairing === 'No',
            intro_video: this.firstFormGroup.value.intro_video ?? '',
            prior_experience: this.secondFormGroup.value.prior_experience ?? '',
            service_experience:
              this.secondFormGroup.value.service_experience ?? '',
            additional_experience:
              this.secondFormGroup.value.additional_experience ?? ''
          };

          console.log(formData);

          this.applicationService
            .createApplication(formData as Application)
            .subscribe({
              next: (application) => this.onSuccess(application),
              error: (err) => this.onError(err)
            });
        },
        error: (err) => {
          console.error('Failed to fetch user details', err);
        }
      });
    }
  }

  /** Opens a confirmation snackbar when an application is successfully submitted.
   * @returns {void}
   */
  private onSuccess(application: Application): void {
    this.router.navigate(['/coworking/']);
    this.snackBar.open('Application Submitted!', '', { duration: 2000 });
  }

  /** Opens a snackbar when there is an error submitting an application.
   * @returns {void}
   */
  private onError(err: any): void {
    this.snackBar.open('Application Failed', '', {
      duration: 2000
    });
  }
}
