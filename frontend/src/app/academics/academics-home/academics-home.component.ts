import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';
import { PermissionService } from 'src/app/permission.service';

@Component({
  selector: 'app-academics-home',
  templateUrl: './academics-home.component.html',
  styleUrls: ['./academics-home.component.css']
})
export class AcademicsHomeComponent implements OnInit {
  /** Route information to be used in Course Routing Module */
  public static Route = {
    path: '',
    title: 'Academics',
    component: AcademicsHomeComponent,
    canActivate: []
  };

  constructor(private gearService: NagivationAdminGearService) {}

  ngOnInit() {
    this.gearService.showAdminGear('academics.*', '*', '', 'academics/admin/');
  }
}
