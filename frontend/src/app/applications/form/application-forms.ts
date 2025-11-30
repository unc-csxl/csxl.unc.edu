import { FormGroup } from '@angular/forms';

// GTA Application Forms

/** Encapsulates the different possible types of form fields. */
export enum FormFieldType {
  SHORT_TEXT,
  LONG_TEXT,
  DROP_DOWN,
  COURSE_PREFERENCE,
  NUMBER
}

/** Represents an application form field. */
export interface ApplicationFormField {
  name: string;
  title: string;
  description: string;
  fieldType: FormFieldType;
  dropdownItems: string[] | undefined;
  required: boolean;
}

// All application forms:

export const GTA_APPLICATION_FORM: ApplicationFormField[] = [
  {
    name: 'program_pursued',
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
    title: 'Possible Course Matches',
    description: `Please **select ALL courses you have completed at UNC or comparably at another institution**. For PhD students, productive RA matches are given higher precedence over TA matches due to the limited funding available for TAships.

Make your selections in order of preference (first choice being strongest preference, and so on).
We will make a best effort for a positive match, but cannot guarantee any specific placement.
    `,
    fieldType: FormFieldType.COURSE_PREFERENCE,
    dropdownItems: undefined,
    required: true
  },
  {
    name: 'prior_experience',
    title: 'Prior TA/LA Experience?',
    description: '',
    fieldType: FormFieldType.LONG_TEXT,
    dropdownItems: undefined,
    required: true
  },
  {
    name: 'intro_video_url',
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
    fieldType: FormFieldType.SHORT_TEXT,
    dropdownItems: undefined,
    required: true
  }
];

export const UTA_APPLICATION_FORM: ApplicationFormField[] = [
  {
    name: 'intro_video_url',
    title: 'Introductory Video',
    description: `
Record a video up to 2-minutes long using your laptop or phone's video recording functionality. Please do not go beyond 2-minutes!
Upload it as an UNLISTED but not private (meaning the public cannot see it, just us) YouTube video. You should spend no more than 10 minutes on recording the video. We promise your first take is good enough and your second take is definitely good enough. Be sure your link works in an incognito window.
This should not be overly formal or overproduced. You should take it lightly, be yourself, and have fun. A selfie-mode recording from your phone or laptop is expected.
Please address:
1. Introduce yourself. (Who are you? How long at UNC? Where are you from?)
2. Why are you applying for a Computer Science Undergraduate Teaching Assistant position?
3. What challenge(s) have you faced in your computer science career at UNC? What strategies or advice would you give to other students confronting similar challenges?
Please add a link to your UNLISTED (NOT PRIVATE!) YouTube video below. Be sure that you can view this link in an Incognito Window or have a friend ensure they were able to view it from their machine. Videos uploaded such that we cannot view them will disqualify your application.    `,
    fieldType: FormFieldType.SHORT_TEXT,
    dropdownItems: undefined,
    required: true
  },
  {
    name: 'prior_experience',
    title: 'Prior Experiences',
    description:
      'What was your prior programming experience before attending UNC?',
    fieldType: FormFieldType.LONG_TEXT,
    dropdownItems: undefined,
    required: true
  },
  {
    name: 'service_experience',
    title: 'Service Experiences',
    description:
      'What experience do you have providing service directly to other people (at jobs or volunteering)? What lessons did you learn or take away from this experience?',
    fieldType: FormFieldType.LONG_TEXT,
    dropdownItems: undefined,
    required: true
  },
  {
    name: 'additional_experience',
    title: 'Additional Experiences',
    description:
      'Outside of anything mentioned above, do you have additional job or working experience?',
    fieldType: FormFieldType.LONG_TEXT,
    dropdownItems: undefined,
    required: true
  },
  {
    name: 'academic_hours',
    title: 'Academic Hours',
    description:
      'How many academic hours are you planning to enroll in next semester?',
    fieldType: FormFieldType.NUMBER,
    dropdownItems: undefined,
    required: true
  },
  {
    name: 'extracurriculars',
    title: 'Extracurriculars',
    description:
      'What extracurricular activities (clubs, jobs, etc.) will you be involved with next semester? About how many hours per week do you estimate each involvement?',
    fieldType: FormFieldType.LONG_TEXT,
    dropdownItems: undefined,
    required: true
  },
  {
    name: 'expected_graduation',
    title: 'Expected Graduation',
    description: 'When do you expect to graduate?',
    fieldType: FormFieldType.DROP_DOWN,
    dropdownItems: [
      '2024 - Fall',
      '2025 - Spring',
      '2025 - Fall',
      '2026 - Spring',
      '2027 - Spring',
      '2027 - Fall',
      '2028 - Spring',
      '2028 - Fall',
      '2029 - Spring',
      '2029 - Fall',
      'Later'
    ],
    required: true
  },
  {
    name: 'program_pursued',
    title: 'Intended Program of Study',
    description:
      'Please select your intended program if you have not yet been accepted to the CS major.',
    fieldType: FormFieldType.DROP_DOWN,
    dropdownItems: [
      'CS Major (BS)',
      'CS Major (BA)',
      'CS Minor',
      'None of the above'
    ],
    required: true
  },
  {
    name: 'other_programs',
    title: 'Other Programs',
    description:
      'If you are pursiing another major / minor outside of CS, please specify here.',
    fieldType: FormFieldType.SHORT_TEXT,
    dropdownItems: [],
    required: true
  },
  {
    name: 'gpa',
    title: 'What is your overall GPA?',
    description: 'Please specify your current GPA to two decimal places.',
    fieldType: FormFieldType.NUMBER,
    dropdownItems: undefined,
    required: true
  },
  {
    name: 'comp_gpa',
    title: 'What is your Computer Science (COMP) GPA?',
    description:
      'This GPA includes all COMP courses and courses required for the major.',
    fieldType: FormFieldType.NUMBER,
    dropdownItems: undefined,
    required: true
  },
  {
    name: 'preferences',
    title: 'TA Course Preferences',
    description:
      'Please select, in order of preference (leftmost is #1 choice), which courses you would like to be considered UTAing for.',
    fieldType: FormFieldType.COURSE_PREFERENCE,
    dropdownItems: undefined,
    required: true
  },
  {
    name: 'comp_227',
    title: 'Preferred Compensation',
    description:
      'It is also possible to receive credit for COMP 227, Effective Peer Teaching In Computer Science, instead of monetary compensation for being a UTA. Students who choose this option will meet with the COMP 227 instructor as a class once a week (must be available Thursdays from 2-3:15pm) to learn about best practices in CS education and how to apply them as UTAs. The time served as a UTA is considered a practicum associated with the course which fulfills the EE general education requirement tag.',
    fieldType: FormFieldType.DROP_DOWN,
    dropdownItems: [
      'Monetary compensation only'
      // 'COMP 227 credit only',
      // 'Open to either 227 credit or compensation'
    ],
    required: true
  }
];
