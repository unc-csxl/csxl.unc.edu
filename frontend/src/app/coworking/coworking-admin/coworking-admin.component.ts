/**
 * The Coworking Admin Component provides the functionality for managing operating hours
 *
 * @author David Foss, Ella Gonzales, Francine Wei, Tobenna Okoli
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  WritableSignal,
  OnInit,
  OnDestroy,
  signal
} from '@angular/core';
import { permissionGuard } from 'src/app/permission.guard';

@Component({
  selector: 'app-coworking-admin',
  templateUrl: './coworking-admin.component.html',
  styleUrls: ['./coworking-admin.component.css']
})
export class CoworkingAdminComponent implements OnInit, OnDestroy {
  isAddingHours: WritableSignal<boolean> = signal(false);
  public static Route = {
    path: 'admin',
    component: CoworkingAdminComponent,
    title: 'CSXL Open Hours Administration',
    canActivate: [permissionGuard('coworking.operating_hours', '*')]
  };

  showAddHoursPanel(): void {
    this.isAddingHours.set(true);
    localStorage.setItem('isAddingHours', String(this.isAddingHours()));
  }

  ngOnInit(): void {
    const savedVisibility = localStorage.getItem('isAddingHours');
    this.isAddingHours.set(savedVisibility === 'true');
  }

  ngOnDestroy(): void {
    localStorage.removeItem('isAddingHours');
  }
}
