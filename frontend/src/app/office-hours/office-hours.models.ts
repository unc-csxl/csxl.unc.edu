/**
 * @author Madelyn Andrews, Sadie Amato, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Section, SectionMember } from '../academics/academics.models';
import { Room } from '../coworking/coworking.models';
import { UserSummary } from '../models.module';

export enum TicketState {
  QUEUED,
  CALLED,
  CLOSED,
  CANCELED
}

export enum TicketType {
  CONCEPTUAL_HELP,
  ASSIGNMENT_HELP
}

export enum OfficeHoursEventType {
  OFFICE_HOURS,
  TUTORING,
  REVIEW_SESSION,
  VIRTUAL_OFFICE_HOURS,
  VIRTUAL_TUTORING,
  VIRTUAL_REVIEW_SESSION
}

export interface Ticket {
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
  type: TicketType;
  creators: { id: number }[]; // check this type ?
}

export interface OfficeHoursEvent {
  id: number;
  oh_section: Section;
  room: Room;
  type: OfficeHoursEventType;
  description: string;
  location_description: string;
  event_date: Date;
  start_time: Date;
  end_time: Date;
}

export interface OfficeHoursEventPartial {
  id: number;
  oh_section: Section | null;
  room: Room | null;
  type: OfficeHoursEventType | null;
  description: string | null;
  location_description: string | null;
  event_date: Date | null;
  start_time: Date | null;
  end_time: Date | null;
}

export interface OfficeHoursEventDraft {
  oh_section: OfficeHoursSectionPartial;
  // room: RoomPartial
  type: OfficeHoursEventType;
  description: string;
  location_description: string;
  event_date: Date;
  start_time: Date;
  end_time: Date;
}

export interface OfficeHoursEventDetails {
  id: number;
  oh_section: Section;
  room: Room;
  type: OfficeHoursEventType;
  description: string;
  location_description: string;
  event_date: Date;
  start_time: Date;
  end_time: Date;
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
