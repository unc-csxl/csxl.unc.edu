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

export interface SignageOfficeHoursJSON {
  id: number;
  mode: string;
  course: string;
  location: string;
  queued: number;
}

export interface SignageAnnouncementJSON {
  title: string;
}

export interface SignageProfileJSON {
  first_name: string;
  last_name: string;
  github_avatar: string;
}

export interface SlowSignageDataJSON {
  newest_news: ArticleOverviewJson[];
  events: EventOverviewJson[];
  top_users: SignageProfileJSON[];
  announcements: SignageAnnouncementJSON[];
}

export interface FastSignageDataJSON {
  active_office_hours: SignageOfficeHoursJSON[];
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

export interface SlowSignageData {
  newest_news: ArticleOverview[];
  newest_events: EventOverview[];
  top_users: SignageProfile[];
  announcements: SignageAnnouncement[];
}

export interface FastSignageData {
  active_office_hours: SignageOfficeHours[];
  available_rooms: string[];
  seat_availability: SeatAvailability[];
}

export interface WeatherData {
  temperature2m: number;
  isDay: number;
  weatherCode: number;
  windSpeed10m: number;
}

export const parseSignageOfficeHoursJSON = (
  json: SignageOfficeHoursJSON
): SignageOfficeHours => {
  return {
    id: json.id,
    course: json.course,
    location: json.mode == 'In-Person' ? json.location : 'Virtual',
    queued: json.queued
  };
};

export const parseSignageProfileJSON = (
  json: SignageProfileJSON
): SignageProfile => {
  return {
    first_name: json.first_name,
    last_name: json.last_name,
    github_avatar: json.github_avatar
  };
};

export const parseSlowSignageDataJSON = (
  json: SlowSignageDataJSON
): SlowSignageData => {
  return {
    newest_news: json.newest_news.map(parseArticleOverviewJson),
    newest_events: json.events.map(parseEventOverviewJson),
    top_users: json.top_users.map(parseSignageProfileJSON),
    announcements: json.announcements
  };
};

export const parseFastSignageDataJSON = (
  json: FastSignageDataJSON
): FastSignageData => {
  return {
    active_office_hours: json.active_office_hours.map(
      parseSignageOfficeHoursJSON
    ),
    available_rooms: json.available_rooms,
    seat_availability: json.seat_availability.map(parseSeatAvailabilityJSON)
  };
};
