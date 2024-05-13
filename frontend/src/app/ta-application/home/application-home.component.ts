import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';

@Component({
  selector: 'application-home',
  templateUrl: './application-home.component.html'
})
export class ApplicationHomeComponent {
  public static Route = {
    path: '',
    component: ApplicationHomeComponent
  };

  constructor(
    protected dialog: MatDialog,
    private router: Router
  ) {}

  completionRedirect(): void {
    this.router.navigate(['/academics/']);
  }
}
