/**
 * The Article Editor Component allows students to read news articles.
 *
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

import { Component, Signal, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NewsService } from '../news.service';
import { ArticleOverview } from 'src/app/welcome/welcome.model';
import { newsResolver } from '../news.resolver';

@Component({
  selector: 'app-article-page',
  templateUrl: './article-page.component.html',
  styleUrl: './article-page.component.css'
})
export class ArticlePageComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: ':slug',
    title: ' ',
    component: ArticlePageComponent,
    resolve: {
      article: newsResolver
    }
  };

  /** Signal to store the current article. */
  article: Signal<ArticleOverview>;

  /** Constructor */
  constructor(
    private route: ActivatedRoute,
    protected newsService: NewsService
  ) {
    const data = this.route.snapshot.data as {
      article: ArticleOverview | null;
    };
    this.article = signal(data.article!);
  }
}
