export interface Application {
  id: number;
  user_id: number;
  user: any;
  academics_hours: string;
  extracurriculars: string;
  program_pursued: string;
  other_programs: string;
  gpa: string;
  comp_gpa: string;
  preferred_courses: string[];
  eligible_courses: string[];
  comp_227: string;
  open_pairing: boolean;
  intro_video: string;
  prior_experience: string;
  service_experience: string;
  additional_experience: string;
  [key: string]: any;
}
