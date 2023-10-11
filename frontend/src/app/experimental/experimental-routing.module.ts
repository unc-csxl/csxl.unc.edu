import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ExperimentalComponent } from './experimental.component';
import { EventDetailsComponent } from './event-details/event-details.component';

const routes: Routes = [
    ExperimentalComponent.Route,
    EventDetailsComponent.Route
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class ExperimentalRoutingModule { }