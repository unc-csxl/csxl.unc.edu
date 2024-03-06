export interface Application {
  id: number;
  user: any;
  section_member: any[];
  intro_video: string;
  prior_experience: string;
  service_experience: string;
  additional_experience: string;
  academics_hours: string;
  extracurriculars: string;
  program_pursued: string;
  other_programs: string;
  gpa: string;
  comp_gpa: string;
  courses_eligible: string[];
  course_preferences: string[];
  comp_227: string;
  open_pairing: boolean;
  [key: string]: any;
}
