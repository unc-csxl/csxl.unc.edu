import { AsyncPipe, CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { AcademicsRoutingModule } from './academics-routing.module';
import { CoursesHomeComponent } from './courses-home/courses-home.component';
import { MatIconModule } from '@angular/material/icon';
import { OfferingsComponent } from './offerings/offerings.component';

@NgModule({
  declarations: [CoursesHomeComponent, OfferingsComponent],
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
    AsyncPipe
  ]
})
export class AcademicsModule {}
