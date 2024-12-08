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
  signal,
  effect
} from '@angular/core';
import { permissionGuard } from 'src/app/permission.guard';
import { OperatingHours } from '../coworking.models';
import { currentTermResolver } from 'src/app/academics/academics.resolver';

@Component({
  selector: 'app-coworking-admin',
  templateUrl: './coworking-admin.component.html',
  styleUrls: ['./coworking-admin.component.css']
})
export class CoworkingAdminComponent implements OnInit, OnDestroy {
  isAddingHours: WritableSignal<boolean> = signal(false);
  selectedOperatingHours: WritableSignal<OperatingHours | null> = signal(null);
  public static Route = {
    path: 'admin',
    component: CoworkingAdminComponent,
    title: 'CSXL Open Hours Administration',
    canActivate: [permissionGuard('coworking.operating_hours', '*')],
    resolve: {
      currentTerm: currentTermResolver
    }
  };

  showAddHoursPanel(): void {
    this.isAddingHours.set(true);
    localStorage.setItem('isAddingHours', String(this.isAddingHours()));
    this.selectedOperatingHours.set(null);
  }

  // Do not pass this function to the calendar, instead pass the return value to the calendar
  // We do this because we're referring to instance properties that don't seem to exist
  selectOperatingHours(): (operatingHours: OperatingHours) => void {
    let isAddingHours = this.isAddingHours;
    let selectedOperatingHours = this.selectedOperatingHours;
    return (operatingHours: OperatingHours) => {
      isAddingHours.set(false);
      localStorage.removeItem('isAddingHours');
      selectedOperatingHours.set(operatingHours);
    };
  }

  ngOnInit(): void {
    const savedVisibility = localStorage.getItem('isAddingHours');
    this.isAddingHours.set(savedVisibility === 'true');
  }

  ngOnDestroy(): void {
    localStorage.removeItem('isAddingHours');
  }
}
