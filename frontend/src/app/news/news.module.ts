/**
 * The News Module couples all features of the News feature into a single
 * unit that can be loaded at once. This decreases load time for the overall
 * application and decouples this feature from other features in the application.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

/* Angular Material Modules */
import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatChipsModule } from '@angular/material/chips';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { NewsRoutingModule } from './news-routing.module';
import { ArticlePageComponent } from './article-page/article-page.component';
import { NewsAdminComponent } from './news-admin/news-admin.component';
import { ArticleEditorComponent } from './article-editor/article-editor.component';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatButtonToggleModule } from '@angular/material/button-toggle';

@NgModule({
  declarations: [
    ArticlePageComponent,
    NewsAdminComponent,
    ArticleEditorComponent
  ],
  imports: [
    CommonModule,
    MatTabsModule,
    MatTableModule,
    MatCardModule,
    MatChipsModule,
    MatDialogModule,
    MatButtonModule,
    MatSelectModule,
    MatFormFieldModule,
    MatInputModule,
    MatPaginatorModule,
    MatListModule,
    MatAutocompleteModule,
    FormsModule,
    ReactiveFormsModule,
    MatIconModule,
    MatTooltipModule,
    RouterModule,
    SharedModule,
    NewsRoutingModule,
    MatSlideToggleModule,
    MatButtonToggleModule
  ]
})
export class NewsModule {}
