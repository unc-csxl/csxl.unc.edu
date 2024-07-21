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
  ArticleOverview,
  ArticleOverviewJson,
  parseArticleOverviewJson
} from '../welcome/welcome.model';

@Injectable({
  providedIn: 'root'
})
export class NewsService {
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
}
