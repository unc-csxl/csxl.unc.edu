/**
 * The My Courses Module couples all features of the My Courses feature,
 * Office Hours feature, and Academics features into a single unit that
 * can be loaded at once. This decreases load time for the overall
 * application and decouples this feature from other features.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MyCoursesRoutingModule } from './my-courses-routing.module';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { MyCoursesPageComponent } from './my-courses-page/my-courses-page.component';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { CourseCardWidget } from './widgets/course-card/course-card.widget';
import { CatalogComponent } from './catalog/catalog.component';
import { MatTabsModule } from '@angular/material/tabs';
import { AllCoursesComponent } from './catalog/course-catalog/course-catalog.component';
import { MatTableModule } from '@angular/material/table';
import { SectionOfferingsComponent } from './catalog/section-offerings/section-offerings.component';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatDialogModule } from '@angular/material/dialog';
import { CourseComponent } from './course/course.component';
import { RosterComponent } from './course/roster/roster.component';
import { MatPaginatorModule } from '@angular/material/paginator';

@NgModule({
  declarations: [
    MyCoursesPageComponent,
    CatalogComponent,
    SectionOfferingsComponent,
    AllCoursesComponent,
    CourseComponent,
    RosterComponent,
    CourseCardWidget
  ],
  imports: [
    CommonModule,
    MyCoursesRoutingModule,
    RouterModule,
    SharedModule,
    MatCardModule,
    MatDividerModule,
    MatButtonModule,
    MatIconModule,
    MatTabsModule,
    MatTableModule,
    MatFormFieldModule,
    MatSelectModule,
    FormsModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatPaginatorModule
  ]
})
export class MyCoursesModule {}
