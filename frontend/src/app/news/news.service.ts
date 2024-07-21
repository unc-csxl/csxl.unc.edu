/**
 * The News Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha
 * @copyright 2024 <agandecha@unc.edu>
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
export class NewsService {
  /** Encapsulated paginators */
  private eventsPaginator: Paginator<ArticleOverview> =
    new Paginator<ArticleOverview>('/api/articles/list');

  /** Constructor */
  constructor(protected http: HttpClient) {}

  /**
   * Returns the article for a given slug.
   * @param slug: Slug of the article.
   * @returns { Observable<ArticleOverview> }
   */
  getArticle(slug: string): Observable<ArticleOverview> {
    return this.http
      .get<ArticleOverviewJson>(`/api/articles/${slug}`)
      .pipe(map(parseArticleOverviewJson));
  }

  /**
   * Retrieves a page of events based on pagination parameters.
   * @param params: Pagination parameters.
   * @returns {Observable<Paginated<ArticleOverview, PaginationParams>>}
   */
  list(params: PaginationParams = DEFAULT_PAGINATION_PARAMS) {
    return this.eventsPaginator.loadPage(params, parseArticleOverviewJson);
  }

  /**
   * Creates a new article.
   * @returns { Observable<ArticleOverview> }
   */
  createArticle(article: ArticleDraft): Observable<ArticleOverview> {
    return this.http
      .post<ArticleOverviewJson>(`/api/articles`, article)
      .pipe(map(parseArticleOverviewJson));
  }

  /**
   * Updates an existing article.
   * @returns { Observable<ArticleOverview> }
   */
  updateArticle(article: ArticleDraft): Observable<ArticleOverview> {
    return this.http
      .put<ArticleOverviewJson>(`/api/articles`, article)
      .pipe(map(parseArticleOverviewJson));
  }

  /**
   * Updates an existing article.
   * @returns { Observable<ArticleOverview> }
   */
  deleteArticle(articleId: number) {
    this.http.delete(`/api/articles/${articleId}`);
  }
}
