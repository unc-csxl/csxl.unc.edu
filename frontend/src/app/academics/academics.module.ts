import { AsyncPipe, CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { AcademicsRoutingModule } from './academics-routing.module';
import { CoursesHomeComponent } from './course-catalog/course-catalog.component';
import { MatIconModule } from '@angular/material/icon';
import { SectionOfferingsComponent } from './section-offerings/section-offerings.component';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { ReactiveFormsModule } from '@angular/forms';
import { AcademicsHomeComponent } from './academics-home/academics-home.component';

@NgModule({
  declarations: [
    CoursesHomeComponent,
    SectionOfferingsComponent,
    AcademicsHomeComponent
  ],
  imports: [
    AcademicsRoutingModule,
    CommonModule,
    MatCardModule,
    MatDividerModule,
    MatListModule,
    MatExpansionModule,
    MatButtonModule,
    MatTableModule,
    MatIconModule,
    MatFormFieldModule,
    MatSelectModule,
    ReactiveFormsModule,
    AsyncPipe
  ]
})
export class AcademicsModule {}
