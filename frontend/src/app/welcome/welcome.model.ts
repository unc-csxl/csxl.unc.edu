import {
  OperatingHours,
  OperatingHoursJSON,
  Room,
  Seat,
  parseOperatingHoursJSON
} from '../coworking/coworking.models';
import {
  EventOverview,
  EventOverviewJson,
  parseEventOverviewJson
} from '../event/event.model';
import { PublicProfile } from '../profile/profile.service';

export enum ArticleState {
  DRAFT = 'Draft',
  PUBLISHED = 'Published',
  ARCHIVED = 'Archived'
}

export interface ArticleDraft {
  id: number | null;
  slug: string;
  state: ArticleState;
  title: string;
  image_url: string;
  synopsis: string;
  body: string;
  published: Date;
  last_modified: Date | null;
  is_announcement: boolean;
  organization_slug: string | null;
  authors: PublicProfile[];
}

export interface ArticleOverviewJson {
  id: number;
  slug: string;
  state: ArticleState;
  title: string;
  image_url: string;
  synopsis: string;
  body: string;
  published: string;
  last_modified: string | null;
  is_announcement: boolean;
  organization_slug: string | null;
  organization_logo: string | null;
  organization_name: string | null;
  authors: PublicProfile[];
}

export interface ArticleOverview {
  id: number;
  slug: string;
  state: ArticleState;
  title: string;
  image_url: string;
  synopsis: string;
  body: string;
  published: Date;
  last_modified: Date | null;
  is_announcement: boolean;
  organization_slug: string | null;
  organization_logo: string | null;
  organization_name: string | null;
  authors: PublicProfile[];
}

export const parseArticleOverviewJson = (
  responseModel: ArticleOverviewJson
): ArticleOverview => {
  return Object.assign({}, responseModel, {
    published: new Date(responseModel.published),
    last_modified: responseModel.last_modified
      ? new Date(responseModel.last_modified)
      : null
  });
};

export interface ReservationOverviewJson {
  start: Date;
  end: Date;
  seats: Seat[];
  room: Room | null;
}

export interface ReservationOverview {
  start: Date;
  end: Date;
  seats: Seat[];
  room: Room | null;
}

export const parseReservationOverviewJson = (
  responseModel: ReservationOverviewJson
): ReservationOverview => {
  return Object.assign({}, responseModel, {
    start: new Date(responseModel.start),
    end: new Date(responseModel.end)
  });
};

export interface WelcomeOverviewJson {
  announcement: ArticleOverviewJson | null;
  latest_news: ArticleOverviewJson[];
  operating_hours: OperatingHoursJSON[];
  upcoming_reservations: ReservationOverviewJson[];
  registered_events: EventOverviewJson[];
}

export interface WelcomeOverview {
  announcement: ArticleOverview | null;
  latest_news: ArticleOverview[];
  operating_hours: OperatingHours[];
  upcoming_reservations: ReservationOverview[];
  registered_events: EventOverview[];
}

export const parseWelcomeOverviewJson = (
  json: WelcomeOverviewJson
): WelcomeOverview => {
  return {
    announcement: json.announcement
      ? parseArticleOverviewJson(json.announcement)
      : null,
    latest_news: json.latest_news.map(parseArticleOverviewJson),
    operating_hours: json.operating_hours.map(parseOperatingHoursJSON),
    upcoming_reservations: json.upcoming_reservations.map(
      parseReservationOverviewJson
    ),
    registered_events: json.registered_events.map(parseEventOverviewJson)
  };
};
