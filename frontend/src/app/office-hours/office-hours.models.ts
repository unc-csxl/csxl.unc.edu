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
  type: TicketType;
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
  description: string;
  location_description: string;
  event_date: string;
  start_time: string;
  end_time: string;
}

export interface OfficeHoursEventPartial {
  id: number;
  oh_section: OfficeHoursSection | null;
  room: Room | null;
  type: OfficeHoursEventType | null;
  description: string | null;
  location_description: string | null;
  event_date: string | null;
  start_time: string | null;
  end_time: string | null;
}

export interface OfficeHoursEventDraft {
  oh_section: OfficeHoursSectionPartial;
  room: RoomPartial; // should this be a room or room partial?
  type: OfficeHoursEventType;
  description: string;
  location_description: string;
  event_date: string;
  start_time: string;
  end_time: string;
}

export interface RoomPartial {
  id: string;
}

export interface OfficeHoursEventDetails {
  id: number;
  oh_section: OfficeHoursSection;
  room: Room;
  type: OfficeHoursEventType;
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
