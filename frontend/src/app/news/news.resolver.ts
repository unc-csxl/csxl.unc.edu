/**
 * The News Resolver allows articles to be injected into the routes
 * of components.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { NewsService } from './news.service';
import { ArticleOverview } from '../welcome/welcome.model';

/** This resolver injects an event into the events detail component. */
export const newsResolver: ResolveFn<ArticleOverview> = (route, state) => {
  return inject(NewsService).getArticle(route.paramMap.get('slug')!);
};
