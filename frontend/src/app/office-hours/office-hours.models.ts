/**
 * @author Madelyn Andrews, Sadie Amato, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Section, SectionMember } from '../academics/academics.models';
import { Room } from '../coworking/coworking.models';

/* Defines the state of an Office Hours Ticket */
export enum TicketState {
  QUEUED,
  CALLED,
  CLOSED,
  CANCELED
}

/* Defines Ticket Type as Assingment or Conceptual */
export enum TicketType {
  CONCEPTUAL_HELP,
  ASSIGNMENT_HELP
}

/* Defines the type of an Office Hours Event */
export enum OfficeHoursEventType {
  OFFICE_HOURS,
  TUTORING,
  REVIEW_SESSION
}

/* Defines the mode of an Office Hours Event */
export enum OfficeHoursEventModeType {
  IN_PERSON,
  VIRTUAL_STUDENT_LINK,
  VIRTUAL_OUR_LINK
}

export interface Ticket {
  id: number;
  oh_event: OfficeHoursEvent;
  type: TicketType;
  state: TicketState;
  description: string;
  created_at: Date;
  called_at: Date;
  closed_at: Date;
  creators: SectionMember[];
  caller: SectionMember | null;
}

export interface TicketDetails {
  id: number;
  oh_event: OfficeHoursEvent;
  type: TicketType;
  state: TicketState;
  description: string;
  have_concerns: boolean;
  caller_notes: string;
  created_at: Date;
  called_at: Date;
  closed_at: Date;
  creators: SectionMember[];
  caller: SectionMember | null;
}

export interface TicketDraft {
  oh_event: OfficeHoursEventPartial;
  description: string;
  type: string;
  creators: { id: number }[]; // check this type ?
}

export interface TicketPartial {
  id: number;
  oh_event: OfficeHoursEventPartial | null;
  type: TicketType | null;
  state: TicketState | null;
  description: string | null;
  have_concerns: boolean | null;
  caller_notes: string | null;
  created_at: Date | null;
  called_at: Date | null;
  closed_at: Date | null;
  creators: SectionMember[] | null;
  caller: SectionMember | null;
}

export interface OfficeHoursEvent {
  id: number;
  oh_section: OfficeHoursSection;
  room: Room;
  type: OfficeHoursEventType;
  mode: OfficeHoursEventModeType;
  description: string;
  location_description: string;
  event_date: string;
  start_time: string;
  end_time: string;
}

export interface OfficeHoursEventPartial {
  id: number;
  oh_section?: OfficeHoursSection | null | undefined;
  room?: Room | null | undefined;
  type?: OfficeHoursEventType | null | undefined;
  mode?: OfficeHoursEventModeType | null | undefined;
  description?: string | null | undefined;
  location_description?: string | null | undefined;
  event_date?: string | null | undefined;
  start_time?: string | null | undefined;
  end_time?: string | null | undefined;
}

export interface OfficeHoursEventDraft {
  oh_section: OfficeHoursSectionPartial;
  room: RoomPartial; // should this be a room or room partial?
  type: OfficeHoursEventType;
  mode: OfficeHoursEventModeType;
  description: string;
  location_description: string;
  event_date: string;
  start_time: string;
  end_time: string;
}

export enum Weekday {
  Monday = 0,
  Tuesday = 1,
  Wednesday = 2,
  Thursday = 3,
  Friday = 4,
  Saturday = 5,
  Sunday = 6
}

// Method to get the abbreviated name of the weekday
export namespace Weekday {
  export function getAbbreviatedName(day: Weekday): string {
    switch (day) {
      case Weekday.Monday:
        return 'Mon';
      case Weekday.Tuesday:
        return 'Tue';
      case Weekday.Wednesday:
        return 'Wed';
      case Weekday.Thursday:
        return 'Thu';
      case Weekday.Friday:
        return 'Fri';
      case Weekday.Saturday:
        return 'Sat';
      case Weekday.Sunday:
        return 'Sun';
      default:
        return '';
    }
  }
}

export interface RoomPartial {
  id: string;
}

export interface OfficeHoursEventDetails {
  id: number;
  oh_section: OfficeHoursSection;
  room: Room;
  type: OfficeHoursEventType;
  mode: OfficeHoursEventModeType;
  description: string;
  location_description: string;
  event_date: string;
  start_time: string;
  end_time: string;
  tickets: Ticket[];
}

export interface OfficeHoursSection {
  id: number;
  title: string;
}

export interface OfficeHoursSectionPartial {
  id: number;
  title: string | null;
}

export interface OfficeHoursSectionDraft {
  title: string;
}

export interface OfficeHoursSectionDetails {
  id: number;
  title: string;
  sections: Section[];
  events: OfficeHoursEvent[];
}

export interface OfficeHoursEventStatus {
  open_tickets_count: number;
  queued_tickets_count: number;
}

export interface StudentOfficeHoursEventStatus {
  open_tickets_count: number;
  queued_tickets_count: number;
  ticket_position: number;
}

export interface OfficeHoursSectionTrailingData {
  number_of_tickets: number;
  number_of_students: number;
  average_wait_time: number;
  standard_deviation_wait_time: number;
  average_ticket_duration: number;
  standard_deviation_ticket_duration: number;
}
