import { Section } from 'src/app/academics/academics.models';

export interface Application {
  id: number;
  user_id: number;
  user: any;
  academic_hours: number;
  extracurriculars: string;
  expected_graduation: string;
  program_pursued: string;
  other_programs: string;
  gpa: number;
  comp_gpa: number;
  preferred_sections: Section[];
  comp_227: string;
  intro_video_url: string;
  prior_experience: string;
  service_experience: string;
  additional_experience: string;
  [key: string]: any;
}
