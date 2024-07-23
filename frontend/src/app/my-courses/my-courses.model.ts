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
}

export interface OfficeHourTicketOverviewJson {
  id: number;
  created_at: string;
  called_at: string | undefined;
  state: string;
  type: string;
  description: string;
  creators: string[];
  caller: string | undefined;
}

export interface OfficeHourTicketOverview {
  id: number;
  created_at: Date;
  called_at: Date | undefined;
  state: string;
  type: string;
  description: string;
  creators: string[];
  caller: string | undefined;
}

export interface OfficeHourQueueOverviewJson {
  id: number;
  type: string;
  start_time: string;
  end_time: string;
  active: OfficeHourTicketOverviewJson | undefined;
  other_called: OfficeHourTicketOverviewJson[];
  queue: OfficeHourTicketOverviewJson[];
}

export interface OfficeHourQueueOverview {
  id: number;
  type: string;
  start_time: Date;
  end_time: Date;
  active: OfficeHourTicketOverview | undefined;
  other_called: OfficeHourTicketOverview[];
  queue: OfficeHourTicketOverview[];
}

export interface OfficeHourEventRoleOverview {
  role: string;
}

export interface OfficeHourGetHelpOverviewJson {
  event_type: string;
  event_mode: string;
  event_start_time: string;
  event_end_time: string;
  ticket: OfficeHourTicketOverviewJson | undefined;
  queue_position: number;
}

export interface OfficeHourGetHelpOverview {
  event_type: string;
  event_mode: string;
  event_start_time: Date;
  event_end_time: Date;
  ticket: OfficeHourTicketOverview | undefined;
  queue_position: number;
}

export interface TicketDraft {
  office_hours_id: number;
  description: string;
  type: string;
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
}

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
    queue: responseModel.queue.map(parseOfficeHourTicketOverviewJson)
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
