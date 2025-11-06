/**
 * The Hiring models defines the shape of hiring data
 * retrieved from the hiring service and the API.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { CatalogSectionIdentity } from '../applications/applications.model';
import { PublicProfile } from '../profile/profile.service';

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
  applicant_id: number;
  status: ApplicationReviewStatus;
  preference: number;
  notes: string;
  applicant_course_ranking: number;
  level: HiringLevel | null;
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

export enum HiringLevelClassification {
  IOR = 'Instructor of Record',
  PHD = 'PhD',
  MS = 'MS',
  UG = 'UG'
}

export interface HiringLevel {
  id: number | null;
  title: string;
  salary: number;
  load: number;
  classification: HiringLevelClassification;
  is_active: boolean;
}

export enum HiringAssignmentStatus {
  DRAFT = 'Draft',
  COMMIT = 'Commit',
  FINAL = 'Final'
}

export interface HiringAssignmentDraft {
  id: number | null;
  user_id: number;
  term_id: string;
  application_review_id: number | null;
  course_site_id: number;
  level: HiringLevel;
  status: HiringAssignmentStatus;
  position_number: string;
  epar: string;
  i9: boolean;
  notes: string;
  created: Date;
  modified: Date;
}

export interface HiringAssignmentOverview {
  id: number | null;
  user: PublicProfile;
  level: HiringLevel;
  status: HiringAssignmentStatus;
  position_number: string;
  epar: string;
  i9: boolean;
  notes: string;
}

export const hiringAssignmentOverviewToDraft = (
  termId: string,
  site: HiringCourseSiteOverview,
  assignment: HiringAssignmentOverview,
  applicationReviewId: number | null
): HiringAssignmentDraft => {
  return {
    id: assignment.id,
    user_id: assignment.user.id,
    term_id: termId,
    course_site_id: site.course_site_id,
    application_review_id: applicationReviewId,
    level: assignment.level,
    status: assignment.status,
    position_number: assignment.position_number,
    epar: assignment.epar,
    i9: assignment.i9,
    notes: assignment.notes,
    created: new Date(), // overwritten anyway
    modified: new Date() // overwritten anyway
  };
};

export interface HiringCourseSiteOverview {
  course_site_id: number;
  sections: CatalogSectionIdentity[];
  instructors: PublicProfile[];
  total_enrollment: number;
  total_cost: number;
  coverage: number;
  assignments: HiringAssignmentOverview[];
  // reviews: ApplicationReviewOverview[];
  // instructor_preferences: PublicProfile[];
}

export interface HiringAdminOverview {
  sites: HiringCourseSiteOverview[];
}

export interface HiringAdminCourseOverview {
  assignments: HiringAssignmentOverview[];
  reviews: ApplicationReviewOverview[];
  instructor_preferences: PublicProfile[];
}

export interface HiringAssignmentSummaryOverview {
  id: number | null;
  application_review_id: number | null;
  course_site_id: number | null;
  course: string;
  user: PublicProfile;
  instructors: string;
  level: HiringLevel;
  status: HiringAssignmentStatus;
  position_number: string;
  epar: string;
  i9: boolean;
  notes: string;
}

export interface ReleasedHiringAssignment {
  course: string;
  instructors: PublicProfile[];
  level_title: string;
}

export interface ApplicationPriority {
  student_priority: number;
  instructor_priority: number;
  course_site_id: number;
  course_title: string;
}

export interface ConflictCheck {
  application_id: number;
  assignments: HiringAssignmentSummaryOverview[];
  priorities: ApplicationPriority[];
}
