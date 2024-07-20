/**
 * The Hiring models defines the shape of hiring data
 * retrieved from the hiring service and the API.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

export interface ApplicationOverview {
  type: string;
  applicant_name: string;
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
}

export interface ApplicationReviewOverview {
  id: number | null;
  application_id: number;
  application: ApplicationOverview;
  status: ApplicationReviewStatus;
  preference: number;
  notes: string;
  applicant_course_ranking: number;
}

export interface HiringStatus {
  not_preferred: ApplicationReviewOverview[];
  not_processed: ApplicationReviewOverview[];
  preferred: ApplicationReviewOverview[];
}

export enum ApplicationReviewStatus {
  NOT_PREFERRED = 'Not Preferred',
  NOT_PROCESSED = 'Not Processed',
  PREFERRED = 'Preferred'
}
