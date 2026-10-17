import { Component, EventEmitter, Input, Output } from '@angular/core';
import { OperatingHours } from '../../coworking.models';
import { PermissionService } from '../../../permission.service';
import {
  operatingHoursDate,
  operatingHoursTime
} from '../../operating-hours-time';

/** The same schedule table is used for active and future hours. */
@Component({
  selector: 'operating-hours-list',
  templateUrl: './operating-hours-list.widget.html',
  standalone: false
})
export class OperatingHoursListWidget {
  @Input({ required: true }) hours: OperatingHours[] = [];
  @Input() allowDelete = false;
  @Input() deletingId: number | null = null;
  @Output() editHours = new EventEmitter<OperatingHours>();
  @Output() deleteHours = new EventEmitter<OperatingHours>();
  columns = ['date', 'start', 'end', 'actions'];
  formatDate = operatingHoursDate;
  formatTime = operatingHoursTime;

  constructor(private permission: PermissionService) {}

  canChange(action: string, hours: OperatingHours): boolean {
    return this.permission.checkSignal(
      `coworking.operating_hours.${action}`,
      `coworking/operating_hours/${hours.id}`
    );
  }
}
