/**
 * The Applications Model defines the shape of applications
 * data from the backend.
 *
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

export interface CatalogSectionIdentity {
  id: number | null;
  subject_code: string;
  course_number: string;
  section_number: string;
}

export interface ApplicationSectionChoice {
  id: number;
  subject_code: string;
  course_number: string;
  section_number: string;
  title: string;
}

export interface Application {
  id: number | null;
  user_id: number;
  term_id: string;
  type: string;
  academic_hours: number | null;
  extracurriculars: string | null;
  expected_graduation: string | null;
  program_pursued: string | null;
  other_programs: string | null;
  gpa: number | null;
  comp_gpa: number | null;
  comp_227: string | null;
  intro_video_url: string | null;
  prior_experience: string | null;
  service_experience: string | null;
  additional_experience: string | null;
  ta_experience: string | null;
  best_moment: string | null;
  desired_improvement: string | null;
  advisor: string | null;
  preferred_sections: CatalogSectionIdentity[];
}
