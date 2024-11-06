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
  OfficeHourQueueOverview,
  OfficeHourQueueOverviewJson,
  parseOfficeHourQueueOverview,
  parseOfficeHoursJson
} from '../my-courses/my-courses.model';
import {
  ArticleOverviewJson,
  ArticleOverview,
  parseArticleOverviewJson
} from '../welcome/welcome.model';

export interface FastSignageDataJson {
  newest_news: ArticleOverviewJson[];
  newest_events: EventOverviewJson[];
  top_users: PublicProfile[];
  announcements: string[];
}

export interface SlowSignageDataJson {
  active_office_hours: OfficeHourQueueOverviewJson[];
  available_rooms: string[];
  seat_availability: SeatAvailabilityJSON[];
}

export interface FastSignageData {
  newest_news: ArticleOverview[] | null;
  newest_events: EventOverview[];
  top_users: PublicProfile[];
  announcements: string[];
}

export interface SlowSignageData {
  active_office_hours: OfficeHourQueueOverview[] | null;
  available_rooms: string[];
  seat_availability: SeatAvailability[];
}

export const parseFastSignageDataJson = (json: FastSignageDataJson): FastSignageData => {
  return {
    newest_news: json.newest_news.map(parseArticleOverviewJson),
    newest_events: json.newest_events.map(parseEventOverviewJson),
    top_users: json.top_users,
    announcements: json.announcements
  };
};

export const parseSlowSignageDataJson = (json: SlowSignageDataJson): SlowSignageData => {
  return {
    active_office_hours: json.active_office_hours.map(
      parseOfficeHourQueueOverview
    ),
    available_rooms: json.available_rooms,
    seat_availability: json.seat_availability.map(parseSeatAvailabilityJSON)
  };
};
