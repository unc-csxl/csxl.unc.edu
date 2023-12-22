import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CoursesHomeComponent } from './course-catalog/course-catalog.component';
import { OfferingsComponent } from './offerings/offerings.component';

const routes: Routes = [CoursesHomeComponent.Route, OfferingsComponent.Route];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AcademicsRoutingModule {}
