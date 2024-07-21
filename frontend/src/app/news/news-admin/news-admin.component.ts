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

  handlePageEvent(e: PageEvent) {
    let paginationParams = this.articlesPage()!.params;
    paginationParams.page = e.pageIndex;
    paginationParams.page_size = e.pageSize;
    this.newsService
      .list(paginationParams)
      .subscribe((page) => this.articlesPage.set(page));
  }
}
