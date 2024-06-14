import { Component, WritableSignal, signal } from '@angular/core';
import { Paginated, PaginationParams, Paginator } from 'src/app/pagination';
import { CourseMemberOverview } from '../../my-courses.model';
import { ActivatedRoute, Router } from '@angular/router';
import { PageEvent } from '@angular/material/paginator';

@Component({
  selector: 'app-roster',
  templateUrl: './roster.component.html',
  styleUrl: './roster.component.css'
})
export class RosterComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'roster',
    title: 'Course',
    component: RosterComponent
  };

  /** Encapsulated roster paginator and params */
  private rosterPaginator: Paginator<CourseMemberOverview>;
  rosterPage: WritableSignal<
    Paginated<CourseMemberOverview, PaginationParams> | undefined
  > = signal(undefined);

  public displayedColumns: string[] = [
    'first_name',
    'last_name',
    'pronouns',
    'email'
  ];

  constructor(private route: ActivatedRoute) {
    console.log(this.route.snapshot);
    let termId = this.route.parent!.snapshot.params['term_id'];
    let courseId = this.route.parent!.snapshot.params['course_id'];

    this.rosterPaginator = new Paginator<CourseMemberOverview>(
      `/api/academics/my-courses/${termId}/${courseId}/roster`
    );

    const params: PaginationParams = {
      page: 0,
      page_size: 25,
      order_by: '',
      filter: ''
    } as PaginationParams;

    this.rosterPaginator.loadPage(params).subscribe((page) => {
      this.rosterPage.set(page);
    });
  }

  handlePageEvent(e: PageEvent) {
    let paginationParams = this.rosterPage()!.params;
    paginationParams.page = e.pageIndex;
    paginationParams.page_size = e.pageSize;
    this.rosterPaginator.loadPage(paginationParams);
  }
}
