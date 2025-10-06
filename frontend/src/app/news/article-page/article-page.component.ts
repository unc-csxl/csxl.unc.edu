/**
 * The Article Editor Component allows students to read news articles.
 *
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

import { Component, OnInit, Signal, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NewsService } from '../news.service';
import { ArticleOverview } from 'src/app/welcome/welcome.model';
import { newsResolver } from '../news.resolver';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';
import { PublicProfile } from 'src/app/profile/profile.service';

@Component({
    selector: 'app-article-page',
    templateUrl: './article-page.component.html',
    styleUrl: './article-page.component.css',
    standalone: false
})
export class ArticlePageComponent implements OnInit {
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
    protected newsService: NewsService,
    private gearService: NagivationAdminGearService
  ) {
    const data = this.route.snapshot.data as {
      article: ArticleOverview | null;
    };
    this.article = signal(data.article!);
  }

  ngOnInit() {
    this.gearService.showAdminGearByPermissionCheck(
      'article.*',
      '*',
      '',
      `/article/${this.article().slug}/edit`
    );
  }

  /** Check if emoji should be displayed for an author (not expired) */
  shouldDisplayEmoji(author: PublicProfile): boolean {
    if (!author.profile_emoji) return false;
    if (!author.emoji_expiration) return true;
    return new Date(author.emoji_expiration) > new Date();
  }

  /** Get display name with emoji if applicable */
  getAuthorDisplayName(author: PublicProfile): string {
    const name = `${author.first_name} ${author.last_name}`;
    if (this.shouldDisplayEmoji(author)) {
      return `${name} ${author.profile_emoji}`;
    }
    return name;
  }
}
