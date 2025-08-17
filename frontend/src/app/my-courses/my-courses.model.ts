/**
 * The My Courses models defines the shape of My Courses data
 * retrieved from the My Courses Service and the API.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Section } from '../academics/academics.models';
import { Paginated, PaginationParams } from '../pagination';
import { PublicProfile } from '../profile/profile.service';

export interface SectionOverview {
  id: number;
  number: string;
  meeting_pattern: string;
  course_site_id: number | null;
  subject_code: string;
  course_number: string;
  section_number: string;
}

export const sectionOverviewToTeachingSectionOverview = (
  sectionOverview: SectionOverview
): TeachingSectionOverview => {
  return {
    id: sectionOverview.id,
    subject_code: sectionOverview.subject_code,
    course_number: sectionOverview.course_number,
    section_number: sectionOverview.section_number,
    title: ''
  };
};

export interface CourseOverview {
  id: string;
  subject_code: string;
  number: string;
  title: string;
  sections: SectionOverview[];
  role: string;
}

export interface TeachingSectionOverview {
  id: number;
  subject_code: string;
  course_number: string;
  section_number: string;
  title: string;
}

export interface TermOverview {
  id: string;
  name: string;
  start: Date;
  end: Date;
  sites: CourseSiteOverview[];
  teaching_no_site: TeachingSectionOverview[];
}

export interface TermOverviewJson {
  id: string;
  name: string;
  start: string;
  end: string;
  sites: CourseSiteOverview[];
  teaching_no_site: TeachingSectionOverview[];
}

export interface CourseMemberOverview {
  id: number;
  pid: number;
  first_name: string;
  last_name: string;
  email: string;
  pronouns: string;
  section_number: string;
  role: string;
}

export interface CourseRosterOverview {
  id: string;
  subject_code: string;
  number: string;
  title: string;
  members: Paginated<CourseMemberOverview, PaginationParams>;
}

export interface OfficeHourEventOverviewJson {
  id: number;
  type: string;
  mode: string;
  description: string;
  location: string;
  location_description: string;
  start_time: string;
  end_time: string;
  queued: number;
  total_tickets: number;
  recurrence_pattern_id: number;
}

export interface OfficeHourEventOverview {
  id: number;
  type: string;
  mode: string;
  description: string;
  location: string;
  location_description: string;
  start_time: Date;
  end_time: Date;
  queued: number;
  total_tickets: number;
  recurrence_pattern_id: number;
}

export interface OfficeHourTicketOverviewJson {
  id: number;
  created_at: string;
  called_at: string | undefined;
  closed_at: string | undefined;
  state: string;
  type: number;
  description: string;
  creators: PublicProfile[];
  caller: PublicProfile | undefined;
  has_concerns: boolean | undefined;
  caller_notes: string | undefined;
}

export interface OfficeHourTicketOverview {
  id: number;
  created_at: Date;
  called_at: Date | undefined;
  closed_at: Date | undefined;
  state: string;
  type: number;
  description: string;
  creators: PublicProfile[];
  caller: PublicProfile | undefined;
  has_concerns: boolean | undefined;
  caller_notes: string | undefined;
}

export interface OfficeHourQueueOverviewJson {
  id: number;
  type: string;
  start_time: string;
  end_time: string;
  active: OfficeHourTicketOverviewJson | undefined;
  other_called: OfficeHourTicketOverviewJson[];
  queue: OfficeHourTicketOverviewJson[];
  personal_tickets_called: number;
  average_minutes: number;
  total_tickets_called: number;
  history: OfficeHourTicketOverviewJson[];
}

export interface OfficeHourQueueOverview {
  id: number;
  type: string;
  start_time: Date;
  end_time: Date;
  active: OfficeHourTicketOverview | undefined;
  other_called: OfficeHourTicketOverview[];
  queue: OfficeHourTicketOverview[];
  personal_tickets_called: number;
  average_minutes: number;
  total_tickets_called: number;
  history: OfficeHourTicketOverview[];
}

export interface OfficeHourEventRoleOverview {
  role: string;
}

export interface OfficeHourGetHelpOverviewJson {
  event_type: string;
  event_mode: string;
  event_start_time: string;
  event_end_time: string;
  event_location: string;
  event_location_description: string;
  ticket: OfficeHourTicketOverviewJson | undefined;
  queue_position: number;
}

export interface OfficeHourGetHelpOverview {
  event_type: string;
  event_mode: string;
  event_start_time: Date;
  event_end_time: Date;
  event_location: string;
  event_location_description: string;
  ticket: OfficeHourTicketOverview | undefined;
  queue_position: number;
}

export interface TicketDraft {
  office_hours_id: number;
  description: string;
  type: number;
}

export interface CourseSiteOverview {
  id: number;
  term_id: string;
  subject_code: string;
  number: string;
  title: string;
  role: string;
  sections: SectionOverview[];
  gtas: PublicProfile[];
  utas: PublicProfile[];
}

export interface NewCourseSite {
  title: string;
  term_id: string;
  section_ids: number[];
}

export interface UpdatedCourseSite {
  id: number;
  title: string;
  term_id: string;
  section_ids: number[];
  gtas: PublicProfile[];
  utas: PublicProfile[];
  minimum_ticket_cooldown: number | null;
  max_tickets_per_day: number | null;
}

export interface CourseSite {
  id: string;
  title: string;
  term_id: string;
}

export interface NewOfficeHoursJson {
  type: number;
  mode: number;
  description: string;
  location_description: string;
  start_time: string;
  end_time: string;
  course_site_id: number;
  room_id: string;
}

export interface NewOfficeHours {
  type: number;
  mode: number;
  description: string;
  location_description: string;
  start_time: Date;
  end_time: Date;
  course_site_id: number;
  room_id: string;
}

export interface NewOfficeHoursRecurrencePattern {
  start_date: Date;
  end_date: Date | null;
  recur_monday: boolean;
  recur_tuesday: boolean;
  recur_wednesday: boolean;
  recur_thursday: boolean;
  recur_friday: boolean;
  recur_saturday: boolean;
  recur_sunday: boolean;
}

export interface OfficeHoursRecurrencePattern {
  id: number;
  start_date: Date;
  end_date: Date | null;
  recur_monday: boolean;
  recur_tuesday: boolean;
  recur_wednesday: boolean;
  recur_thursday: boolean;
  recur_friday: boolean;
  recur_saturday: boolean;
  recur_sunday: boolean;
}

export interface OfficeHoursJson {
  id: number;
  type: number;
  mode: number;
  description: string;
  location_description: string;
  start_time: string;
  end_time: string;
  course_site_id: number;
  room_id: string;
  recurrence_pattern_id: number | null;
  recurrence_pattern: OfficeHoursRecurrencePattern | null;
}

export interface OfficeHours {
  id: number;
  type: number;
  mode: number;
  description: string;
  location_description: string;
  start_time: Date;
  end_time: Date;
  course_site_id: number;
  room_id: string;
  recurrence_pattern_id: number | null;
  recurrence_pattern: OfficeHoursRecurrencePattern | null;
}

export interface OfficeHourStatisticsFilterDataJson {
  students: PublicProfile[];
  staff: PublicProfile[];
  term_start: string;
  term_end: string;
}

export interface OfficeHourStatisticsFilterData {
  students: PublicProfile[];
  staff: PublicProfile[];
  term_start: string;
  term_end: string;
}

export interface OfficeHoursTicketStatistics {
  total_tickets: number;
  total_tickets_weekly: number;
  average_wait_time: number;
  average_duration: number;
  total_conceptual: number;
  total_assignment: number;
}

/** Defines the general model for statistics pagination parameters expected by the backend. */
export interface OfficeHourStatisticsPaginationParams extends URLSearchParams {
  page: number;
  page_size: number;
  filter: string;
  student_ids: string;
  staff_ids: string;
  range_start: string;
  range_end: string;
}

export const DefaultOfficeHourStatisticsPaginationParams = {
  page: 0,
  page_size: 25,
  student_ids: '',
  staff_ids: '',
  range_start: '',
  range_end: ''
} as OfficeHourStatisticsPaginationParams;
/**
 * Function that converts an TermOverviewJson response model to a
 * TermOverview model.
 *
 * This function is needed because the API response will return certain
 * objects (such as `Date`s) as strings. We need to convert this to
 * TypeScript objects ourselves.
 */
export const parseTermOverviewJson = (
  responseModel: TermOverviewJson
): TermOverview => {
  return Object.assign({}, responseModel, {
    start: new Date(responseModel.start),
    end: new Date(responseModel.end)
  });
};

export const parseTermOverviewJsonList = (
  responseModels: TermOverviewJson[]
): TermOverview[] => {
  return responseModels.map(parseTermOverviewJson);
};

export const parseOfficeHourEventOverviewJson = (
  responseModel: OfficeHourEventOverviewJson
): OfficeHourEventOverview => {
  return Object.assign({}, responseModel, {
    start_time: new Date(responseModel.start_time),
    end_time: new Date(responseModel.end_time)
  });
};

export const parseOfficeHourEventOverviewJsonList = (
  responseModel: OfficeHourEventOverviewJson[]
): OfficeHourEventOverview[] => {
  return responseModel.map((model) => parseOfficeHourEventOverviewJson(model));
};

export const parseOfficeHourTicketOverviewJson = (
  responseModel: OfficeHourTicketOverviewJson
): OfficeHourTicketOverview => {
  return Object.assign({}, responseModel, {
    created_at: new Date(responseModel.created_at),
    called_at: responseModel.called_at
      ? new Date(responseModel.called_at)
      : undefined,
    closed_at: responseModel.closed_at
      ? new Date(responseModel.closed_at)
      : undefined
  });
};

export const parseOfficeHourQueueOverview = (
  responseModel: OfficeHourQueueOverviewJson
): OfficeHourQueueOverview => {
  return Object.assign({}, responseModel, {
    start_time: new Date(responseModel.start_time),
    end_time: new Date(responseModel.end_time),
    active: responseModel.active
      ? parseOfficeHourTicketOverviewJson(responseModel.active)
      : undefined,
    other_called: responseModel.other_called.map(
      parseOfficeHourTicketOverviewJson
    ),
    queue: responseModel.queue.map(parseOfficeHourTicketOverviewJson),
    history: responseModel.history.map(parseOfficeHourTicketOverviewJson)
  });
};

export const parseOfficeHourGetHelpOverviewJson = (
  responseModel: OfficeHourGetHelpOverviewJson
): OfficeHourGetHelpOverview => {
  return Object.assign({}, responseModel, {
    ticket: responseModel.ticket
      ? parseOfficeHourTicketOverviewJson(responseModel.ticket)
      : undefined,
    event_start_time: new Date(responseModel.event_start_time),
    event_end_time: new Date(responseModel.event_end_time)
  });
};

export const parseNewOfficeHoursJson = (
  responseModel: NewOfficeHoursJson
): NewOfficeHoursJson => {
  return Object.assign({}, responseModel, {
    start_time: new Date(responseModel.start_time),
    end_time: new Date(responseModel.end_time)
  });
};

export const parseOfficeHoursJson = (
  responseModel: OfficeHoursJson
): OfficeHours => {
  return Object.assign({}, responseModel, {
    start_time: new Date(responseModel.start_time),
    end_time: new Date(responseModel.end_time)
  });
};

export const parseOfficeHourStatisticsFilterDataJson = (
  responseModel: OfficeHourStatisticsFilterDataJson
): OfficeHourStatisticsFilterData => {
  return Object.assign({}, responseModel, {
    term_start: new Date(responseModel.term_start),
    term_end: new Date(responseModel.term_end)
  });
};
