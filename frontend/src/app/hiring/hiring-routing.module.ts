/**
 * The Hiring Routing Module holds all of the routes that are children
 * to the path /hiring/...
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HiringPreferencesComponent } from './hiring-preferences/hiring-preferences.component';
import { HiringAdminComponent } from './hiring-admin/hiring-admin.component';
import { LevelsAdminComponent } from './levels-admin/levels-admin.component';
import { LevelEditorComponent } from './levels-admin/level-editor/level-editor.component';
import { HiringSummaryComponent } from './hiring-summary/hiring-summary.component';
import { HiringAssignmentsComponent } from './hiring-assignments/hiring-assignments.component';
import { HiringPageComponent } from './hiring-page/hiring-page.component';

const routes: Routes = [
  HiringAdminComponent.Route,
  HiringSummaryComponent.Route,
  LevelsAdminComponent.Route,
  LevelEditorComponent.Route,
  {
    path: ':courseSiteId',
    component: HiringPageComponent,
    children: [
      HiringPreferencesComponent.Route,
      HiringAssignmentsComponent.Route
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HiringRoutingModule {}
