import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AmbassadorXlListComponent } from './ambassador-xl/list/ambassador-xl-list.component';
import { AmbassadorPageComponent } from './ambassador-home.component';

const routes: Routes = [
  {
    path: '',
    component: AmbassadorPageComponent,
    children: [AmbassadorXlListComponent.Route]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AmbassadorHomeRoutingModule {}
