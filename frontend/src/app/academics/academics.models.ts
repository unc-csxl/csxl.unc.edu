/**
 * These helper modules define the structure of data that is accessible
 * at the `/api/academics` endpoints.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023
 * @license MIT
 */

import { Seat } from '../coworking/coworking.models';
import { TimeRange } from '../time-range';

/** Defines a Course */
export interface Course {
  id: string;
  subject_code: string;
  number: string;
  title: string;
  description: string;
  credit_hours: number;
  sections: Section[] | null;
}

/** Defines a Course Section */
export interface Section {
  id: number | null;
  course_id: string;
  number: string;
  term_id: string;
  meeting_pattern: string;
  course: Course | null;
  term: Term | null;
  staff: SectionMember[] | null;
  lecture_room: Room | null;
  office_hour_rooms: Room[] | null;
  override_title: string;
  override_description: string;
  enrolled: number;
  total_seats: number;
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

/** Defines a Section Member Partial */
export interface SectionMemberPartial {
  id: number;
  member_role: RosterRole | null;
}

/** Defines a Room */
export interface Room {
  id: string;
  nickname: string;
  building: string | null;
  room: string | null;
  capacity: number | null;
  reservable: boolean | null;
  seats: Seat[] | null;
}

/** Defines a Roster Role */
export enum RosterRole {
  STUDENT = 0,
  UTA = 1,
  GTA = 2,
  INSTRUCTOR = 3
}
