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
export class ExperimentalRoutingModule { }