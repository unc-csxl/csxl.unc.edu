import {
  SeatAvailability,
  SeatAvailabilityJSON,
  parseSeatAvailabilityJSON
} from '../coworking/coworking.models';
import {
  EventOverview,
  parseEventOverviewJson,
  EventOverviewJson
} from '../event/event.model';
import {
  ArticleOverviewJson,
  ArticleOverview,
  parseArticleOverviewJson
} from '../welcome/welcome.model';

export interface SignageOfficeHoursJson {
  id: number;
  mode: string;
  course: string;
  location: string;
  queued: number;
}

export interface SignageAnnouncementJson {
  title: string;
}

export interface SignageProfileJson {
  first_name: string;
  last_name: string;
  github_avatar: string;
}

export interface SlowSignageDataJson {
  newest_news: ArticleOverviewJson[];
  events: EventOverviewJson[];
  top_users: SignageProfileJson[];
  announcements: SignageAnnouncementJson[];
}

export interface FastSignageDataJson {
  active_office_hours: SignageOfficeHoursJson[];
  available_rooms: string[];
  seat_availability: SeatAvailabilityJSON[];
}

export interface SignageOfficeHours {
  id: number;
  course: string;
  location: string;
  queued: number;
}

export interface SignageAnnouncement {
  title: string;
}

export interface SignageProfile {
  first_name: string;
  last_name: string;
  github_avatar: string;
}

export enum AvailabeRoom {
  SN139,
  SN144,
  SN146,
  SN135,
  SN137,
  SN141,
  SN147
}

export interface SlowSignageData {
  newest_news: ArticleOverview[];
  newest_events: EventOverview[];
  top_users: SignageProfile[];
  announcements: SignageAnnouncement[];
}

export interface FastSignageData {
  active_office_hours: SignageOfficeHours[];
  available_rooms: AvailabeRoom[];
  seat_availability: SeatAvailability[];
}

export interface WeatherData {
  temperature: number;
  isDay: number;
  weatherCode: number;
  windSpeed: number;
}

export const parseSignageOfficeHoursJson = (
  json: SignageOfficeHoursJson
): SignageOfficeHours => {
  return {
    id: json.id,
    course: json.course,
    location: json.mode == 'In-Person' ? json.location : 'Virtual',
    queued: json.queued
  };
};

export const parseSignageProfileJson = (
  json: SignageProfileJson
): SignageProfile => {
  return {
    first_name: json.first_name,
    last_name: json.last_name,
    github_avatar: json.github_avatar
  };
};

export const parseAvailableRoomJson = (json: string): AvailabeRoom => {
  return AvailabeRoom[json as keyof typeof AvailabeRoom];
};

export const parseSlowSignageDataJson = (
  json: SlowSignageDataJson
): SlowSignageData => {
  return {
    newest_news: json.newest_news.map(parseArticleOverviewJson),
    newest_events: json.events.map(parseEventOverviewJson),
    top_users: json.top_users.map(parseSignageProfileJson),
    announcements: json.announcements
  };
};

export const parseFastSignageDataJson = (
  json: FastSignageDataJson
): FastSignageData => {
  return {
    active_office_hours: json.active_office_hours.map(
      parseSignageOfficeHoursJson
    ),
    available_rooms: json.available_rooms.map(parseAvailableRoomJson),
    seat_availability: json.seat_availability.map(parseSeatAvailabilityJSON)
  };
};
