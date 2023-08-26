import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

/* HTTP and Auth */
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { HttpRequestInterceptor } from './navigation/http-request.interceptor';
import { JwtModule } from '@auth0/angular-jwt';

/* Angular UI Dependencies */
import { NgForOf } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LayoutModule } from '@angular/cdk/layout';

/* Material UI Dependencies */
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
import { RouterModule } from '@angular/router';

/* UI Widgets */
import { CoworkingTopCard } from './widgets/coworking-top-card/coworking-top-card.widget';
import { CoworkingDropInCard } from './widgets/coworking-dropin-card/coworking-dropin-card.widget';
import { CoworkingReserveCard } from './widgets/coworking-reserve-card/coworking-reserve-card.widget';
import { CoworkingPageComponent } from './coworking/coworking-page/coworking-page.component';
import { ReservationEditorComponent } from './coworking/reservation-editor/reservation-editor.component';
import { CoworkingTentativeDropInCard } from './widgets/coworking-tentative-dropin-card/coworking-tentative-dropin-card.widget';
import { CoworkingInProgressDropInCard } from './widgets/coworking-inprogress-dropin-card/coworking-inprogress-dropin-card.widget';
import { CoworkingExpiredDropInCard } from './widgets/coworking-expired-dropin-card/coworking-expired-dropin-card.widget';
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
    CoworkingPageComponent,

    /* Widgets */
    CoworkingTopCard,
    CoworkingDropInCard,
    CoworkingReserveCard,
    ReservationEditorComponent,
    CoworkingTentativeDropInCard,
    CoworkingInProgressDropInCard,
    CoworkingExpiredDropInCard,
    CoworkingHoursCard,
    CoworkingHoursCardDialog,
  ],
  imports: [
    /* Angular */
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    NgForOf,
    AppRoutingModule,
    LayoutModule,
    ReactiveFormsModule,

    /* Material UI */
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
    FormsModule,
    RouterModule,
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