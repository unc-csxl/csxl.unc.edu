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
import { of } from 'rxjs';

/** This resolver injects an event into the events detail component. */
export const newsResolver: ResolveFn<ArticleOverview | null> = (
  route,
  state
) => {
  let slug = route.paramMap.get('slug')!;
  if (slug === 'new') return of(null);
  return inject(NewsService).getArticle(route.paramMap.get('slug')!);
};
