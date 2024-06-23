/**
 * The My Courses Routing Module holds all of the routes that are children
 * to the path /my-courses/...
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MyCoursesPageComponent } from './my-courses-page/my-courses-page.component';
import { CatalogComponent } from './catalog/catalog.component';
import { AllCoursesComponent } from './catalog/course-catalog/course-catalog.component';
import { SectionOfferingsComponent } from './catalog/section-offerings/section-offerings.component';
import { CourseComponent } from './course/course.component';
import { RosterComponent } from './course/roster/roster.component';
import { OfficeHoursPageComponent } from './course/office-hours/office-hours-page/office-hours-page.component';
import { OfficeHoursQueueComponent } from './course/office-hours/office-hours-queue/office-hours-queue.component';
import { OfficeHoursGetHelpComponent } from './course/office-hours/office-hours-get-help/office-hours-get-help.component';
import { SettingsComponent } from './course/settings/settings.component';

const routes: Routes = [
  MyCoursesPageComponent.Route,
  {
    path: 'catalog',
    component: CatalogComponent,
    children: [AllCoursesComponent.Route, SectionOfferingsComponent.Route]
  },
  {
    path: 'course/:course_site_id',
    component: CourseComponent,
    children: [
      RosterComponent.Route,
      SettingsComponent.Route,
      OfficeHoursPageComponent.Route,
      OfficeHoursQueueComponent.Route,
      OfficeHoursGetHelpComponent.Route
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MyCoursesRoutingModule {}
