import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppTitleStrategy } from './app-title.strategy';
import { GateComponent } from './gate/gate.component';
import { HomeComponent } from './home/home.component';
import { ProfileEditorComponent } from './profile/profile-editor/profile-editor.component';
import { CoworkingPageComponent } from './coworking/coworking-home/coworking-home.component';
import { AmbassadorPageComponent } from './coworking/ambassador-home/ambassador-home.component';
import { AboutComponent } from './about/about.component';


const routes: Routes = [
  HomeComponent.Route,
  AboutComponent.Route,
  ProfileEditorComponent.Route,
  GateComponent.Route,
  CoworkingPageComponent.Route,
  AmbassadorPageComponent.Route,
  { path: 'coworking', title: 'Cowork in the XL', loadChildren: () => import('./coworking/coworking.module').then(m => m.CoworkingModule) },
  { path: 'admin', title: 'Admin', loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule) },
  { path: 'organizations', title: 'CS Organizations', loadChildren: () => import('./organization/organization.module').then(m => m.OrganizationModule) },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    scrollPositionRestoration: 'enabled',
    anchorScrolling: 'enabled'
  })],
  exports: [RouterModule],
  providers: [AppTitleStrategy.Provider]
})
export class AppRoutingModule { }