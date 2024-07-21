/**
 * The News Routing Module holds all of the routes that are children
 * to the path /news/...
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ArticlePageComponent } from './article-page/article-page.component';
import { NewsAdminComponent } from './news-admin/news-admin.component';
import { ArticleEditorComponent } from './article-editor/article-editor.component';

const routes: Routes = [
  NewsAdminComponent.Route,
  ArticlePageComponent.Route,
  ArticleEditorComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class NewsRoutingModule {}
