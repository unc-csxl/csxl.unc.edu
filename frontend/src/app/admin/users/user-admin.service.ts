import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Paginated, PaginationParams } from 'src/app/pagination';
import { Profile } from 'src/app/models.module';

@Injectable({ providedIn: 'root' })
export class UserAdminService {

  constructor(protected http: HttpClient) { }

  list(params: PaginationParams) {
    let paramStrings = {
      page: params.page.toString(),
      page_size: params.page_size.toString(),
      order_by: params.order_by,
      filter: params.filter,
    };
    let query = new URLSearchParams(paramStrings);
    return this.http.get<Paginated<Profile>>("/api/admin/users?" + query.toString());
  }

}