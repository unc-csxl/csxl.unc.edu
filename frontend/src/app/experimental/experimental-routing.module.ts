import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ExperimentalComponent } from './experimental.component';

const routes: Routes = [
    ExperimentalComponent.Route
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class ExperimentalRoutingModule { }