/**
 * The Course Catalog enables users to view all COMP courses at UNC.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import { coursesResolver } from '../academics.resolver';
import { Course } from '../academics.models';
import { ActivatedRoute } from '@angular/router';
import { AcademicsService } from '../academics.service';
import {
  animate,
  state,
  style,
  transition,
  trigger
} from '@angular/animations';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';

@Component({
  selector: 'app-courses-home',
  templateUrl: './course-catalog.component.html',
  styleUrls: ['./course-catalog.component.css'],
  animations: [
    trigger('detailExpand', [
      state('collapsed,void', style({ height: '0px', minHeight: '0' })),
      state('expanded', style({ height: '*' })),
      transition(
        'expanded <=> collapsed',
        animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')
      )
    ])
  ]
})
export class CoursesHomeComponent implements OnInit {
  /** Route information to be used in Course Routing Module */
  public static Route = {
    path: 'catalog',
    title: 'Course Catalog',
    component: CoursesHomeComponent,
    canActivate: [],
    resolve: { courses: coursesResolver }
  };

  /** Store list of Courses */
  public courses: Course[];

  /** Store the columns to display in the table */
  public displayedColumns: string[] = ['code', 'title'];
  /** Store the columns to display when extended */
  public columnsToDisplayWithExpand = [...this.displayedColumns, 'expand'];
  /** Store the element where the dropdown is currently active */
  public expandedElement: Course | null = null;

  /** Constructor for the course catalog page. */
  constructor(
    private route: ActivatedRoute,
    public academicsService: AcademicsService,
    private gearService: NagivationAdminGearService
  ) {
    // Initialize data from resolvers
    const data = this.route.snapshot.data as {
      courses: Course[];
    };

    this.courses = data.courses;
  }

  ngOnInit() {
    this.gearService.showAdminGearByPermissionCheck(
      'academics.*',
      '*',
      '',
      'academics/admin/course'
    );
  }
}
