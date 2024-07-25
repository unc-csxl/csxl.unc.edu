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
import { HiringPageComponent } from './hiring-page/hiring-page.component';
import { HiringAdminComponent } from './hiring-admin/hiring-admin.component';
import { LevelsAdminComponent } from './levels-admin/levels-admin.component';
import { LevelEditorComponent } from './levels-admin/level-editor/level-editor.component';

const routes: Routes = [
  HiringAdminComponent.Route,
  LevelsAdminComponent.Route,
  HiringPageComponent.Route,
  LevelEditorComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HiringRoutingModule {}
