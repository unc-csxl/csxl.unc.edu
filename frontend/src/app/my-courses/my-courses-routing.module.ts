/**
 * The My Courses Routing Module holds all of the routes that are children
 * to the path /my-courses/...
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MyCoursesPageComponent } from './my-courses-page/my-courses-page.component';
import { CatalogComponent } from './catalog/catalog.component';

const routes: Routes = [MyCoursesPageComponent.Route, CatalogComponent.Route];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MyCoursesRoutingModule {}
