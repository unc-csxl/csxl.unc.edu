/**
 * The Signage Routing Module just holds the route for the signage compoent.
 * 
 * @author Andrew Lockard, Will Zahrt
 * @copyright 2024
 * @license MIT
 */

import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { SignageComponent } from "./signage.component";

const routes: Routes = [
    SignageComponent.Route,
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class SignageRoutingModule {}