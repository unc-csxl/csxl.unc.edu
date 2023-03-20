import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Profile } from 'src/app/profile/profile.service';
import { UserAdminService } from 'src/app/admin/users/user-admin.service';
import { permissionGuard } from 'src/app/permission.guard';

import { Paginated } from 'src/app/pagination';
import { PageEvent } from '@angular/material/paginator';


@Component({
  selector: 'app-admin-users-list',
  templateUrl: './admin-users-list.component.html',
  styleUrls: []
})
export class AdminUsersListComponent {

  public page: Paginated<Profile>;

  public displayedColumns: string[] = ['first_name', 'last_name', 'pronouns', 'email'];

  private static PaginationParams = { page: 0, page_size: 25, order_by: 'first_name', filter: '' };

  public static Route = {
    path: 'users',
    component: AdminUsersListComponent,
    title: 'User Administration',
    canActivate: [permissionGuard('user.list', 'user/')],
    resolve: { page: () => inject(UserAdminService).list(AdminUsersListComponent.PaginationParams) }
  }

  constructor(
    private userAdminService: UserAdminService,
    private router: Router,
    route: ActivatedRoute,
  ) {
    let data = route.snapshot.data as { page: Paginated<Profile> };
    this.page = data.page;
  }

  onClick(user: Profile) {
    this.router.navigate(['admin', 'users', user.id]);
  }

  handlePageEvent(e: PageEvent) {
    let paginationParams = this.page.params;
    paginationParams.page = e.pageIndex;
    paginationParams.page_size = e.pageSize;
    this.userAdminService.list(paginationParams).subscribe((page) => this.page = page)
  }

}