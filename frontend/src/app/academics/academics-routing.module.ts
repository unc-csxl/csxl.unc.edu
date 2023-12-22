import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CoursesHomeComponent } from './course-catalog/course-catalog.component';
import { SectionOfferingsComponent } from './section-offerings/section-offerings.component';

const routes: Routes = [
  CoursesHomeComponent.Route,
  SectionOfferingsComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AcademicsRoutingModule {}
