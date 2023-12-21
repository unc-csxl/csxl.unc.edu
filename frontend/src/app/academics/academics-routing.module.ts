import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CoursesHomeComponent } from './courses-home/courses-home.component';
import { OfferingsComponent } from './offerings/offerings.component';

const routes: Routes = [CoursesHomeComponent.Route, OfferingsComponent.Route];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AcademicsRoutingModule {}
