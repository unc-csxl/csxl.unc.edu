import { Component, Input, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { OperatingHours } from 'src/app/coworking/coworking.models';
import { PermissionService } from 'src/app/permission.service';

@Component({
  selector: 'coworking-operating-hours-panel',
  templateUrl: './operating-hours-panel.widget.html',
  styleUrls: ['./operating-hours-panel.widget.css']
})
export class CoworkingHoursCard implements OnDestroy {
  @Input() operatingHours!: OperatingHours[];
  @Input() openOperatingHours?: OperatingHours;

  private createHoursPermissionSubscription: Subscription;
  createHoursPermission: boolean = false;

  private deleteHoursPermissionSubscription: Subscription;
  deleteHoursPermission: boolean = false;

  constructor(public permission: PermissionService) {
    this.createHoursPermissionSubscription = permission
      .check('coworking.operating_hours.create', 'coworking/operating_hours')
      .subscribe((permission) => (this.createHoursPermission = permission));

    this.deleteHoursPermissionSubscription = permission
      .check('coworking.operating_hours.delete', 'coworking/operating_hours/*')
      .subscribe((permission) => (this.deleteHoursPermission = permission));
  }

  ngOnDestroy(): void {
    this.createHoursPermissionSubscription.unsubscribe();
    this.deleteHoursPermissionSubscription.unsubscribe();
  }
}
