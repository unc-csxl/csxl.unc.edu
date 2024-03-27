import { SectionMember } from '../academics/academics.models';
import { Room } from '../coworking/coworking.models';
import { UserSummary } from '../models.module';
import { Section } from '../academics/academics.models';

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

export enum EventType {
  OFFICE_HOURS,
  TUTORING,
  REVIEW_SESSION,
  VIRTUAL_OFFICE_HOURS,
  VIRTUAL_TUTORING,
  VIRTUAL_REVIEW_SESSION
}

export interface TicketDetails {
  id: number;
  oh_event: Event;
  type: TicketType;
  state: TicketState;
  description: string;
  have_concerns: boolean;
  caller_notes: string;
  created_at: Date;
  called_at: Date;
  closed_at: Date;
  caller: SectionMember | null;
  creators: SectionMember[];
}

export interface TicketDraft {
  oh_event: EventPartial;
  description: string;
  type: TicketType;
  creators: { id: number }[]; // check this type ?
}

export interface Event {
  id: number;
  oh_section: OfficeHoursSection;
  room: Room;
  type: EventType;
  description: string;
  location_description: string;
  event_date: Date;
  start_time: Date;
  end_time: Date;
}

export interface EventPartial {
  id: number;
  oh_section: Section | null;
  room: Room | null;
  type: EventType | null;
  description: string | null;
  location_description: string | null;
  event_date: Date | null;
  start_time: Date | null;
  end_time: Date | null;
}

export interface OfficeHoursSectionDraft {
  title: string;
}

export interface OfficeHoursSection {
  id: number;
  title: string;
}

export interface OfficeHoursSectionDetails {
  id: number;
  title: string;
  sections: Section[];
}
