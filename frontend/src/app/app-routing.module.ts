import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppTitleStrategy } from './app-title.strategy';
import { GateComponent } from './gate/gate.component';
import { HomeComponent } from './home/home.component';
import { OrganizationsComponent } from './organizations/organizations.component';
import { ProfileEditorComponent } from './profile/profile-editor/profile-editor.component';
import { ProfilePageComponent } from './profile/profile-page/profile-page.component';
import { OrgDetailsComponent } from './org-details/org-details.component';
import { EventEditorComponent } from './events/event-editor/event-editor.component';
import { OrgEditorComponent } from './org-editor/org-editor.component';
import { OrgRosterComponent } from './org-roster/org-roster.component';
import { CoworkingPageComponent } from './coworking/coworking-page/coworking-page.component';
import { ReservationEditorComponent } from './coworking/reservation-editor/reservation-editor.component';
import { EventsPageComponent } from './events/events-page/events-page.component';

const routes: Routes = [
  HomeComponent.Route,
  ProfileEditorComponent.Route,
  ProfilePageComponent.Route,
  GateComponent.Route,
  { path: 'admin', title: 'Admin', loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule) },
  OrganizationsComponent.Route,
  EventsPageComponent.Route,
  OrgDetailsComponent.Route,
  EventEditorComponent.Route,
  OrgEditorComponent.Route,
  OrgRosterComponent.Route,
  CoworkingPageComponent.Route,
  ReservationEditorComponent.Route
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