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
import { EventPageComponent } from './event-page/event-page.component';

const routes: Routes = [
    EventPageComponent.Route,
    EventDetailsComponent.Route
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class EventRoutingModule { }