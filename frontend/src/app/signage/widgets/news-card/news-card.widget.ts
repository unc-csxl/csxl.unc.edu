/**
 * The News Card displays details for events in the paginated list.
 *
 * @author Will Zahrt <wzahrt@unc.edu>
 * @author Andrew Lockard <andrew.lockard15@gmail.com>
 * @copyright 2024
 * @license MIT
 */

import { Component, effect, input } from '@angular/core';
import { ArticleOverview } from '../../../welcome/welcome.model';

@Component({
  selector: 'news-card',
  templateUrl: './news-card.widget.html',
  styleUrl: './news-card.widget.css'
})
export class NewsCardWidget {
  articles = input<ArticleOverview[]>([]);
  shownArticle: number = 0;

  constructor() {
    effect(() => {
      /**
       * If the articles input changes, we want to switch the view back to the first one,
       * this prevents the edge case where the articles array is updated to be shorter,
       * and the shownArticle index is no longer in the new array
       */
      this.articles();
      this.shownArticle = 0;
    });
  }

  /**
   * Rotates the shown article to the next one in the list,
   * making sure to loop back to the first
   */
  nextArticle() {
    this.shownArticle = (this.shownArticle + 1) % this.articles().length;
  }
}
