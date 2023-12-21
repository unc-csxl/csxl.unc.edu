import { TimeRange } from '../coworking/coworking.models';

/** Defines a Course */
export interface Course {
  id: string;
  subject_code: string;
  number: string;
  title: string;
  description: string;
  sections: Section[] | null;
}

/** Defines a Course Section */
export interface Section {
  id: number;
  course_id: string;
  number: string;
  term_id: string;
  meeting_pattern: string;
  course: Course | null;
  term: Term | null;
  staff: SectionMember[] | null;
}

/** Defines a Term */
export interface Term extends TimeRange {
  id: string;
  name: string;
  course_sections: Section[] | null;
}

/** Defines a Section Member */
export interface SectionMember {
  id: number | null;
  first_name: string;
  last_name: string;
  pronouns: string;
  member_role: RosterRole;
}

/** Defines a Roster Role */
export enum RosterRole {
  STUDENT = 0,
  UTA = 1,
  GTA = 2,
  INSTRUCTOR = 3
}
