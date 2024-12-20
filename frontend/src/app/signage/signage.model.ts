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
import { PublicProfile } from '../profile/profile.service';
import {
  ArticleOverviewJson,
  ArticleOverview,
  parseArticleOverviewJson
} from '../welcome/welcome.model';

export interface SlowSignageDataJson {
  newest_news: ArticleOverviewJson[];
  events: EventOverviewJson[];
  top_users: PublicProfile[];
  announcement_titles: string[];
}

export interface SignageOfficeHours {
  id: number;
  mode: string;
  course: string;
  location: string;
  queued: number;
}

export interface FastSignageDataJson {
  active_office_hours: SignageOfficeHours[];
  available_rooms: string[];
  seat_availability: SeatAvailabilityJSON[];
}

export interface SlowSignageData {
  newest_news: ArticleOverview[];
  newest_events: EventOverview[];
  top_users: PublicProfile[];
  announcement_titles: string[];
}

export interface FastSignageData {
  active_office_hours: SignageOfficeHours[];
  available_rooms: string[];
  seat_availability: SeatAvailability[];
}

export const parseSlowSignageDataJson = (json: SlowSignageDataJson): SlowSignageData => {
  return {
    newest_news: json.newest_news.map(parseArticleOverviewJson),
    newest_events: json.events.map(parseEventOverviewJson),
    top_users: json.top_users,
    announcement_titles: json.announcement_titles
  };
};

export const parseFastSignageDataJson = (json: FastSignageDataJson): FastSignageData => {
  return {
    active_office_hours: json.active_office_hours,
    available_rooms: json.available_rooms,
    seat_availability: json.seat_availability.map(parseSeatAvailabilityJSON)
  };
};
