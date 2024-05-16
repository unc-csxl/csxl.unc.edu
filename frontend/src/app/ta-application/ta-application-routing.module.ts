/**
 * The TA Application Routing Module holds all of the routes that are children
 * to the path /ta-application/...
 *
 * @author Ben Goulet
 * @copyright 2024
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UndergradApplicationComponent } from './uta-application/uta-application.component';
import { ApplicationHomeComponent } from './home/application-home.component';

const routes: Routes = [
  ApplicationHomeComponent.Route,
  UndergradApplicationComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ApplicationsRoutingModule {}
