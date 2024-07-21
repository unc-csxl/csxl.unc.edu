/**
 * The News Admin Component allows the admin to modify news articles.
 *
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

import { Component, Signal, WritableSignal, signal } from '@angular/core';
import { ArticleOverview } from 'src/app/welcome/welcome.model';
import { NewsService } from '../news.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { permissionGuard } from 'src/app/permission.guard';
import {
  DEFAULT_PAGINATION_PARAMS,
  Paginated,
  PaginationParams
} from 'src/app/pagination';
import { PageEvent } from '@angular/material/paginator';
import { tap } from 'rxjs';

@Component({
  selector: 'app-news-admin',
  templateUrl: './news-admin.component.html',
  styleUrl: './news-admin.component.css'
})
export class NewsAdminComponent {
  /** Articles List */
  public articlesPage: WritableSignal<
    Paginated<ArticleOverview, PaginationParams> | undefined
  > = signal(undefined);

  public displayedColumns: string[] = ['title'];

  /** Route information to be used in Organization Routing Module */
  public static Route = {
    path: 'admin',
    component: NewsAdminComponent,
    title: 'News Administration',
    canActivate: [permissionGuard('article.*', '*')]
  };

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private newsService: NewsService
  ) {
    this.newsService.list(DEFAULT_PAGINATION_PARAMS).subscribe((page) => {
      this.articlesPage.set(page);
    });
  }

  /** Delete an article.*/
  deleteArticle(article: ArticleOverview): void {
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this article?',
      'Delete',
      { duration: 15000 }
    );
    confirmDelete.onAction().subscribe(() => {
      this.newsService.deleteArticle(article.id).subscribe(() => {
        this.newsService.list(DEFAULT_PAGINATION_PARAMS).subscribe((page) => {
          this.articlesPage.set(page);
        });
        this.snackBar.open('This article has been deleted.', '', {
          duration: 2000
        });
      });
    });
  }

  handlePageEvent(e: PageEvent) {
    let paginationParams = this.articlesPage()!.params;
    paginationParams.page = e.pageIndex;
    paginationParams.page_size = e.pageSize;
    this.newsService
      .list(paginationParams)
      .subscribe((page) => this.articlesPage.set(page));
  }
}
