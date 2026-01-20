import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  standalone: false
})
export class AdminComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'admin',
    title: 'Admin',
    component: AdminComponent
  };

  facts$: Observable<AdminFacts>;

  constructor(protected http: HttpClient) {
    this.facts$ = this.http.get<AdminFacts>('/api/admin/facts');
  }
}

interface AdminFacts {
  users: number;
  roles: number;
  terms: number;
  courses: number;
  sections: number;
  rooms: number;
  organizations: number;
  articles: number;
}
