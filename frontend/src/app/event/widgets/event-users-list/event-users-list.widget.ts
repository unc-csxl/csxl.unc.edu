/**
 * The Event Users List widget displays the registered users
 * for an event in a paginated.
 *
 * @author Jade Keegan
 * @copyright 2023
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import { PageEvent } from '@angular/material/paginator';
import { Paginated } from 'src/app/pagination';
import { Profile } from 'src/app/models.module';
import { EventService } from '../../event.service';
import { Event } from '../../event.model';

@Component({
  selector: 'event-users-list',
  templateUrl: './event-users-list.widget.html',
  styleUrls: ['./event-users-list.widget.css']
})
export class EventUsersList implements OnInit {
  @Input() event!: Event;
  page!: Paginated<Profile>;

  public displayedColumns: string[] = ['name', 'pronouns', 'email'];

  private static PaginationParams = {
    page: 0,
    page_size: 10,
    order_by: 'first_name',
    filter: ''
  };

  constructor(private eventService: EventService) {}

  ngOnInit() {
    this.eventService
      .getRegisteredUsersForEvent(
        this.event.id!,
        EventUsersList.PaginationParams
      )
      .subscribe((page) => (this.page = page));
  }

  handlePageEvent(e: PageEvent) {
    let paginationParams = this.page.params;
    paginationParams.page = e.pageIndex;
    paginationParams.page_size = e.pageSize;
    this.eventService
      .getRegisteredUsersForEvent(this.event.id!, paginationParams)
      .subscribe((page) => (this.page = page));
  }
}
