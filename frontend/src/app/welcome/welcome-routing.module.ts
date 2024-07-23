/**
 * The Welcome Routing Module holds all of the routes that are children
 * to the path /welcome/...
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WelcomePageComponent } from './welcome-page/welcome-page.component';

const routes: Routes = [WelcomePageComponent.Route];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WelcomeRoutingModule {}
