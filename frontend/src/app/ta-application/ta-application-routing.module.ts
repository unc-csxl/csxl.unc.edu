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
import { ApplicationComponent } from './application-home/application-home.component';
import { UndergradApplicationComponent } from './uta-application/uta-application.component';

const routes: Routes = [
  ApplicationComponent.Route,
  UndergradApplicationComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ApplicationsRoutingModule {}
