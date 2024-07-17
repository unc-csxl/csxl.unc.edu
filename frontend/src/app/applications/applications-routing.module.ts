/**
 * The Applications Routing Module holds all of the routes that are children
 * to the path /apply/...
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ApplicationFormComponent } from './form/application-form.component';

const routes: Routes = [ApplicationFormComponent.Route];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ApplicationsRoutingModule {}
