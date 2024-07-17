import {
  FormControl,
  FormGroup,
  FormGroupDirective,
  Validators
} from '@angular/forms';

export interface ApplicationForm {
  groups: FormGroup[];
}

// GTA Application Forms
export enum FormFieldType {
  SHORT_TEXT,
  LONG_TEXT,
  DROP_DOWN,
  COURSE_PREFERENCE
}

export interface ApplicationFormField {
  name: string;
  title: string;
  description: string;
  fieldType: FormFieldType;
  dropdownItems: string[] | undefined;
  required: boolean;
}

const GTAApplicationForm: ApplicationFormField[] = [
  {
    name: 'program',
    title: 'Which program are you enrolled in?',
    description:
      'PhD students who have completed all requirements except for dissertation defense, please select PhD (ABD).',
    fieldType: FormFieldType.DROP_DOWN,
    dropdownItems: ['PhD', 'PhD (ABD)', 'MS', 'BS/MS'],
    required: true
  },
  {
    name: 'advisor',
    title: 'Graduate Advisor',
    description: '',
    fieldType: FormFieldType.SHORT_TEXT,
    dropdownItems: undefined,
    required: true
  },
  {
    name: 'preferences',
    title: 'TA Course Preferences',
    description:
      'In the event we cannot match you with an RAship, please select the courses you would prefer to work with in order of highest preference to least preference.',
    fieldType: FormFieldType.COURSE_PREFERENCE,
    dropdownItems: undefined,
    required: true
  },
  {
    name: 'prior-ta-experience',
    title: 'Prior TA/LA Experience?',
    description: '',
    fieldType: FormFieldType.LONG_TEXT,
    dropdownItems: undefined,
    required: true
  },
  {
    name: 'video-url',
    title: 'Introductory Video for TAship Eligibility',
    description: `
Record a video up to 5-minutes long using your laptop or phone's video recording functionality. Please do not go beyond 5-minutes!

Upload it as an UNLISTED but *not* private (meaning the public cannot see it, just us) YouTube video. You should spend no more than 10 minutes on recording the video. We promise your first take is good enough and your second take is *definitely* good enough. Be sure your link works in an incognito window.

This should not be overly formal or overproduced. You should take it lightly, be yourself, and have fun. A selfie-mode recording from your phone or laptop is expected.

Please address:

1. Introduce yourself. (Who are you? How long at UNC? Where are you from?)
2. What prior Teaching Assistant / Tutoring / Teaching experience do you have?
3. Why are you applying for a Computer Science Teaching Assistant position? What course(s) do you believe you are most appropriate to be matched with and why? 

Please add a link to your *UNLISTED* (NOT PRIVATE!) YouTube video below. Be sure that you can view this link in an Incognito Window or have a friend ensure they were able to view it from their machine. Videos uploaded such that we cannot view them will disqualify your application.
    `,
    fieldType: FormFieldType.LONG_TEXT,
    dropdownItems: undefined,
    required: true
  }
];

const gtaApplicationFormGroup = () => {
  let formGroup = new FormGroup({});
  for (let field of GTAApplicationForm) {
    formGroup.addControl(
      field.name,
      new FormControl('', field.required ? [Validators.required] : [])
    );
  }
  return formGroup;
};
