import { Component } from '@angular/core';
import { permissionGuard } from 'src/app/permission.guard';
import { OperatingHoursService } from './operating-hours.service';
import { OperatingHours } from '../coworking.models';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

@Component({
  selector: 'app-operating-hours',
  templateUrl: './operating-hours.component.html',
  styleUrl: './operating-hours.component.css',
  standalone: false
})
export class OperatingHoursComponent {
  public static Route = {
    path: 'operating-hours',
    component: OperatingHoursComponent,
    title: 'Operating Hours',
    canActivate: [
      permissionGuard(
        'coworking.operating_hours.*',
        'coworking/operating_hours'
      )
    ]
  };

  operatingHours: OperatingHours[] = [];

  constructor(
    protected operatingHoursService: OperatingHoursService,
    protected snackBar: MatSnackBar,
    protected router: Router
  ) {
    this.fetchOperatingHours();
  }

  fetchOperatingHours() {
    this.operatingHoursService.getOperatingHours().subscribe((result) => {
      this.operatingHours = result;
    });
  }

  newOperatingHours() {
    this.router.navigateByUrl('/coworking/operating-hours/new');
  }

  deleteOperatingHours(id: number) {
    this.operatingHoursService.deleteOperatingHours(id).subscribe({
      next: () => {
        this.fetchOperatingHours();
      },
      error: (err) => {
        this.snackBar.open(`${err.error.message}`, '', {
          duration: 2000
        });
      }
    });
  }
}
