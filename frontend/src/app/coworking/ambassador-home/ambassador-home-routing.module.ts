import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AmbassadorXLComponent } from './ambassador-xl/ambassador-xl.component';
import { AmbassadorPageComponent } from './ambassador-home.component';
import { AmbassadorRoomComponent } from './ambassador-room/ambassador-room.component';

const routes: Routes = [
  {
    path: '',
    component: AmbassadorPageComponent,
    children: [AmbassadorXLComponent.Route, AmbassadorRoomComponent.Route]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AmbassadorHomeRoutingModule {}
