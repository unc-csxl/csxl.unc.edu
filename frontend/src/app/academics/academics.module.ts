import { AsyncPipe, CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { AcademicsRoutingModule } from './academics-routing.module';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { ReactiveFormsModule } from '@angular/forms';
import { AcademicsHomeComponent } from './academics-home/academics-home.component';
import { AcademicsAdminComponent } from './academics-admin/academics-admin.component';
import { MatTabsModule } from '@angular/material/tabs';
import { AdminSectionComponent } from './academics-admin/section/admin-section.component';
import { AdminCourseComponent } from './academics-admin/course/admin-course.component';
import { AdminTermComponent } from './academics-admin/term/admin-term.component';
import { CourseEditorComponent } from './academics-admin/course/course-editor/course-editor.component';
import { MatInputModule } from '@angular/material/input';
import { TermEditorComponent } from './academics-admin/term/term-editor/term-editor.component';
import { SectionEditorComponent } from './academics-admin/section/section-editor/section-editor.component';
import { AdminRoomComponent } from './academics-admin/room/admin-room.component';
import { RoomEditorComponent } from './academics-admin/room/room-editor/room-editor.component';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { SharedModule } from '../shared/shared.module';

@NgModule({
  declarations: [
    AcademicsHomeComponent,
    AcademicsAdminComponent,
    AdminSectionComponent,
    AdminCourseComponent,
    AdminTermComponent,
    CourseEditorComponent,
    TermEditorComponent,
    SectionEditorComponent,
    AdminRoomComponent,
    RoomEditorComponent
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
    MatTabsModule,
    MatInputModule,
    MatCheckboxModule,
    AsyncPipe,
    SharedModule
  ]
})
export class AcademicsModule {}
