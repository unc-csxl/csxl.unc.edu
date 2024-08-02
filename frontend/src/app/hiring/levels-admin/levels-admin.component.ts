import { Component, signal, WritableSignal } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { HiringService } from '../hiring.service';
import { HiringLevel } from '../hiring.models';

@Component({
  selector: 'app-levels-admin',
  templateUrl: './levels-admin.component.html',
  styleUrl: './levels-admin.component.css'
})
export class LevelsAdminComponent {
  /** Route for the routing module */
  public static Route = {
    path: 'levels',
    title: 'Hiring Levels',
    component: LevelsAdminComponent
  };

  /** Columns to display on the table */
  public displayedColumns: string[] = [
    'title',
    'classification',
    'salary',
    'load',
    'active'
  ];

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    protected hiringService: HiringService
  ) {}

  createLevel(): void {
    this.router.navigate(['hiring', 'levels', 'new', 'edit']);
  }

  editLevel(level: HiringLevel): void {
    this.router.navigate(['hiring', 'levels', level.id, 'edit']);
  }
}
