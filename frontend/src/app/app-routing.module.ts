import { NgModule } from '@angular/core';
import { ActivatedRouteSnapshot, ResolveFn, RouterModule, Routes, TitleStrategy } from '@angular/router';
import { of } from 'rxjs';
import { AppTitleStrategy } from './app-title.strategy';
import { GateComponent } from './authentication/gate.component';
import { isAuthenticated as isAuthenticated } from './authentication/gate.guard';
import { HomeComponent } from './home/home.component';
import { ProfileEditorComponent } from './profile/profile-editor/profile-editor.component';
import { profileResolver } from './profile/profile.resolver';


const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'gate', component: GateComponent, canActivate: [isAuthenticated], resolve: { profile: profileResolver } },
  ProfileEditorComponent.Route
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    scrollPositionRestoration: 'enabled',
    anchorScrolling: 'enabled'
  })],
  exports: [RouterModule],
  providers: [
    { provide: TitleStrategy, useClass: AppTitleStrategy }
  ]
})
export class AppRoutingModule {}