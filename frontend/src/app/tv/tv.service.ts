/**
 * The TV Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Will Zahrt
 * @copyright 2024
 * @license MIT
 */

import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import {
  ArticleDraft,
  ArticleOverview,
  ArticleOverviewJson,
  parseArticleOverviewJson
} from '../welcome/welcome.model';
import {
  DEFAULT_PAGINATION_PARAMS,
  PaginationParams,
  Paginator
} from '../pagination';

@Injectable({
  providedIn: 'root'
})
export class TvService {
  /** Encapsulated paginators */
  private eventsPaginator: Paginator<ArticleOverview> =
    new Paginator<ArticleOverview>('/api/articles/list');

  /** Constructor */
  constructor(protected http: HttpClient) {}

  /**
   * Retrieves a page of events based on pagination parameters.
   * @param params: Pagination parameters.
   * @returns {Observable<Paginated<ArticleOverview, PaginationParams>>}
   */
  list(params: PaginationParams = DEFAULT_PAGINATION_PARAMS) {
    return this.eventsPaginator.loadPage(params, parseArticleOverviewJson);
  }
}
