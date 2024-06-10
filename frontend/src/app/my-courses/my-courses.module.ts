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

@NgModule({
  declarations: [MyCoursesPageComponent],
  imports: [CommonModule, MyCoursesRoutingModule, RouterModule, SharedModule]
})
export class MyCoursesModule {}
