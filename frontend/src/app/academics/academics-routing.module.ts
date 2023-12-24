import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CoursesHomeComponent } from './course-catalog/course-catalog.component';
import { SectionOfferingsComponent } from './section-offerings/section-offerings.component';
import { AcademicsHomeComponent } from './academics-home/academics-home.component';
import { AcademicsAdminComponent } from './academics-admin/academics-admin.component';
import { AdminTermComponent } from './academics-admin/term/admin-term.component';
import { AdminCourseComponent } from './academics-admin/course/admin-course.component';
import { AdminSectionComponent } from './academics-admin/section/admin-section.component';

const routes: Routes = [
  {
    path: 'admin',
    component: AcademicsAdminComponent,
    children: [
      AdminTermComponent.Route,
      AdminCourseComponent.Route,
      AdminSectionComponent.Route
    ]
  },
  AcademicsHomeComponent.Route,
  CoursesHomeComponent.Route,
  SectionOfferingsComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AcademicsRoutingModule {}
