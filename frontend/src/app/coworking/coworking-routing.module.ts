import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CoworkingPageComponent } from './coworking-page/coworking-page.component';
import { AmbassadorPageComponent } from './ambassador-page/ambassador-page.component';

const routes: Routes = [
  CoworkingPageComponent.Route,
  AmbassadorPageComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CoworkingRoutingModule { }
