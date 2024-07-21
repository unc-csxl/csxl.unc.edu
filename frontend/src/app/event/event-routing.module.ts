/**
 * The Event Routing Module holds all of the routes that are children
 * to the path /events/...
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EventDetailsComponent } from './event-details/event-details.component';
import { EventEditorComponent } from './event-editor/event-editor.component';
import { EventsPageComponent } from './events-page/events-page.component';

const routes: Routes = [
  EventsPageComponent.Route,
  EventDetailsComponent.Route,
  EventEditorComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EventRoutingModule {}
