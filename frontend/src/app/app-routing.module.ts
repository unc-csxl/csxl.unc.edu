import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppTitleStrategy } from './app-title.strategy';
import { GateComponent } from './gate/gate.component';
import { HomeComponent } from './home/home.component';
import { OrganizationsComponent } from './organizations/organizations.component';
import { ProfileEditorComponent } from './profile/profile-editor/profile-editor.component';
import { ProfilePageComponent } from './profile/profile-page/profile-page.component';
import { EventsComponent } from './events/events.component';


const routes: Routes = [
  HomeComponent.Route,
  ProfileEditorComponent.Route,
  ProfilePageComponent.Route,
  GateComponent.Route,
  { path: 'admin', title: 'Admin', loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule) },
  OrganizationsComponent.Route,
  EventsComponent.Route
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    scrollPositionRestoration: 'enabled',
    anchorScrolling: 'enabled'
  })],
  exports: [RouterModule],
  providers: [AppTitleStrategy.Provider]
})
export class AppRoutingModule {}