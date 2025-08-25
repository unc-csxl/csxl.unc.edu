import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppTitleStrategy } from './app-title.strategy';
import { GateComponent } from './gate/gate.component';
import { HomeComponent } from './home/home.component';
import { AboutComponent } from './about/about.component';
import { SignageComponent } from './signage/signage.component';
import { SamplePageComponent } from './sample/page/sample.component';

const routes: Routes = [
  SamplePageComponent.Route,
  HomeComponent.Route,
  AboutComponent.Route,
  GateComponent.Route,
  {
    path: 'signage',
    title: 'XL Signage',
    loadChildren: () =>
      import('./signage/signage.module').then((m) => m.SignageModule)
  },
  {
    path: 'coworking',
    title: 'Cowork in the XL',
    loadChildren: () =>
      import('./coworking/coworking.module').then((m) => m.CoworkingModule)
  },
  {
    path: 'profile',
    title: 'Profile',
    loadChildren: () =>
      import('./profile/profile.module').then((m) => m.ProfileModule)
  },
  {
    path: 'academics',
    title: 'Academics',
    loadChildren: () =>
      import('./academics/academics.module').then((m) => m.AcademicsModule)
  },
  {
    path: 'admin',
    title: 'Admin',
    loadChildren: () =>
      import('./admin/admin.module').then((m) => m.AdminModule)
  },
  {
    path: 'organizations',
    title: 'CS Organizations',
    loadChildren: () =>
      import('./organization/organization.module').then(
        (m) => m.OrganizationModule
      )
  },
  {
    path: 'events',
    title: 'Experimental',
    loadChildren: () =>
      import('./event/event.module').then((m) => m.EventModule)
  },
  {
    path: '',
    title: 'My Courses',
    loadChildren: () =>
      import('./my-courses/my-courses.module').then((m) => m.MyCoursesModule)
  },
  {
    path: '',
    title: 'My Courses',
    loadChildren: () =>
      import('./my-courses/my-courses.module').then((m) => m.MyCoursesModule)
  },
  {
    path: 'hiring',
    title: 'Hiring',
    loadChildren: () =>
      import('./hiring/hiring.module').then((m) => m.HiringModule)
  },
  {
    path: 'welcome',
    title: 'Welcome to the CSXL',
    loadChildren: () =>
      import('./welcome/welcome.module').then((m) => m.WelcomeModule)
  },
  {
    path: 'article',
    title: 'Articles',
    loadChildren: () => import('./news/news.module').then((m) => m.NewsModule)
  },
  {
    path: 'apply',
    title: 'Applications',
    loadChildren: () =>
      import('./applications/applications.module').then(
        (m) => m.ApplicationsModule
      )
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      scrollPositionRestoration: 'enabled',
      anchorScrolling: 'enabled'
    })
  ],
  exports: [RouterModule],
  providers: [AppTitleStrategy.Provider]
})
export class AppRoutingModule {}
