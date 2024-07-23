/**
 * The Profile Routing Module holds all of the routes that are children
 * to the path /profile/...
 *
 * @author Jade Keegan
 * @copyright 2023
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProfileEditorComponent } from './profile-editor/profile-editor.component';
import { ProfilePageComponent } from './profile-page/profile-page.component';
import { PublicProfilePageComponent } from './public-profile-page/public-profile-page.component';

const routes: Routes = [
  ProfileEditorComponent.Route,
  ProfilePageComponent.Route,
  PublicProfilePageComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProfileRoutingModule {}
