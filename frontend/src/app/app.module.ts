import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

/* HTTP and Auth */
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { HttpRequestInterceptor } from './navigation/http-request.interceptor';
import { JwtModule } from '@auth0/angular-jwt';

/* UI / Material Dependencies */
import { NgForOf } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { LayoutModule } from '@angular/cdk/layout';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatSliderModule } from '@angular/material/slider';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTabsModule } from '@angular/material/tabs';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatGridListModule } from '@angular/material/grid-list';
import { FormsModule } from '@angular/forms';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatSelectModule } from '@angular/material/select';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatChipsModule } from "@angular/material/chips";

/* Application Specific */
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavigationComponent } from './navigation/navigation.component';
import { ErrorDialogComponent } from './navigation/error-dialog/error-dialog.component';
import { HomeComponent } from './home/home.component';
import { GateComponent } from './gate/gate.component';
import { ProfileEditorComponent } from './profile/profile-editor/profile-editor.component';
import { OrganizationFilterPipe } from './organizations/org-filter/org-filter.pipe';
import { ProfilePageComponent } from './profile/profile-page/profile-page.component';
import { EventsFilterPipe } from './events/events-filter/events-filter.pipe';
import { ProfileEventsFilterPipe } from './profile/profile-page/profile-events-filter/event-filter.pipe';
import { OrgDetailsComponent } from './organizations/org-details/org-details.component';
import { EventEditorComponent } from './events/event-editor/event-editor.component';
import { OrganizationsPageComponent } from './organizations/organizations-page/organizations-page.component';
import { OrgEditorComponent } from './organizations/org-editor/org-editor.component';
import { OrgRosterComponent } from './organizations/org-roster/org-roster.component';

/* UI Widgets */
import { SocialMediaIcon } from './widgets/social-media-icon/social-media-icon.widget';
import { OrganizationCard } from './widgets/organization-card/organization-card.widget';
import { SearchBar } from './widgets/search-bar/search-bar.widget';
import { ProfileAboutCard } from './widgets/profile-about-card/profile-about-card.widget';
import { ProfileEventsCard } from './widgets/profile-events-card/profile-events-card.widget';
import { ProfileEventDropdown } from './widgets/profile-event-dropdown/profile-event-dropdown.widget';
import { ProfileOrganizationsCard } from './widgets/profile-organizations-card/profile-organizations-card.widget';
import { EventDropdown } from './widgets/event-dropdown/event-dropdown.widget';
import { OrgDetailsInfoCard } from './widgets/org-details-info-card/org-details-info-card.widget';
import { OrgDetailsExecMembersCard } from './widgets/org-details-exec-members-card/org-details-exec-members-card.widget';
import { OrgDetailsEventsCard } from './widgets/org-details-events-card/org-details-events-card.widget';
import { RosterDropdown } from './widgets/roster-dropdown/roster-dropdown.widget';
import { RosterListCard } from './widgets/roster-list-card/roster-list-card.widget';
import { OrgDetailsRosterCard } from './widgets/org-details-roster-card/org-details-roster-card.widget';
import { RosterAddMemberCard } from './widgets/roster-add-member-card/roster-add-member-card.widget';
import { CoworkingTopCard } from './widgets/coworking-top-card/coworking-top-card.widget';
import { CoworkingDropInCard } from './widgets/coworking-dropin-card/coworking-dropin-card.widget';
import { CoworkingReserveCard } from './widgets/coworking-reserve-card/coworking-reserve-card.widget';
import { CoworkingPageComponent } from './coworking/coworking-page/coworking-page.component';
import { ReservationEditorComponent } from './coworking/reservation-editor/reservation-editor.component';
import { CoworkingTentativeDropInCard } from './widgets/coworking-tentative-dropin-card/coworking-tentative-dropin-card.widget';
import { CoworkingInProgressDropInCard } from './widgets/coworking-inprogress-dropin-card/coworking-inprogress-dropin-card.widget';
import { CoworkingExpiredDropInCard } from './widgets/coworking-expired-dropin-card/coworking-expired-dropin-card.widget';
import { EventsPageComponent } from './events/events-page/events-page.component';
import { CoworkingHoursCard } from './widgets/coworking-hours-card/coworking-hours-card.widget';
import { CoworkingHoursCardDialog } from './widgets/coworking-hours-card/coworking-hours-card-dialog/coworking-hours-card-dialog.widget';


@NgModule({
  declarations: [
    AppComponent,
    NavigationComponent,
    ErrorDialogComponent,
    HomeComponent,
    GateComponent,
    ProfileEditorComponent,
    OrganizationFilterPipe,
    ProfilePageComponent,
    ProfileEventsFilterPipe,
    EventsFilterPipe,
    OrgDetailsComponent,
    EventEditorComponent,
    OrgEditorComponent,
    CoworkingPageComponent,

    SocialMediaIcon,
    OrganizationCard,
    SearchBar,
    ProfileAboutCard,
    ProfileEventsCard,
    ProfileEventDropdown,
    ProfileOrganizationsCard,
    EventDropdown,
    OrgDetailsInfoCard,
    OrgDetailsExecMembersCard,
    OrgDetailsEventsCard,
    OrgRosterComponent,
    RosterDropdown,
    RosterListCard,
    OrgDetailsRosterCard,
    RosterAddMemberCard,
    CoworkingTopCard,
    CoworkingDropInCard,
    CoworkingReserveCard,
    ReservationEditorComponent,
    CoworkingTentativeDropInCard,
    CoworkingInProgressDropInCard,
    CoworkingExpiredDropInCard,
    EventsPageComponent,
    OrganizationsPageComponent,
    CoworkingHoursCard,
    CoworkingHoursCardDialog
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    NgForOf,
    AppRoutingModule,
    LayoutModule,
    ReactiveFormsModule,
    MatButtonModule,
    MatCardModule,
    MatDialogModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    MatProgressBarModule,
    MatSidenavModule,
    MatSliderModule,
    MatSnackBarModule,
    MatTabsModule,
    MatToolbarModule,
    MatGridListModule,
    MatExpansionModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatSelectModule,
    FormsModule,
    MatExpansionModule,
    MatTooltipModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatAutocompleteModule,
    MatCheckboxModule,
    MatChipsModule,
    JwtModule.forRoot({
      config: {
        tokenGetter: () => {
          return localStorage.getItem("bearerToken")
        }
      }
    }),
  ],
  providers: [{
    provide: HTTP_INTERCEPTORS,
    useClass: HttpRequestInterceptor,
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }