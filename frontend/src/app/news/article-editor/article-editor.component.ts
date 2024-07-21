/**
 * The Article Editor Component allows writers to edit or create articles.
 *
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

import { Component } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { newsResolver } from '../news.resolver';
import {
  ArticleDraft,
  ArticleOverview,
  ArticleState,
  BLANK_ARTICLE_DRAFT
} from 'src/app/welcome/welcome.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { NewsService } from '../news.service';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { PublicProfile } from 'src/app/profile/profile.service';

@Component({
  selector: 'app-article-editor',
  templateUrl: './article-editor.component.html',
  styleUrl: './article-editor.component.css'
})
export class ArticleEditorComponent {
  /** Route information to be used in Organization Routing Module */
  public static Route: Route = {
    path: ':slug/edit',
    component: ArticleEditorComponent,
    title: 'Organization Editor',
    canActivate: [permissionGuard('article.*', '*')],
    resolve: {
      article: newsResolver
    }
  };

  articleState = ArticleState;

  /** Stores the article.  */
  public article: ArticleOverview | null;

  /** Article Editor Form */
  public articleForm = this.formBuilder.group({
    title: new FormControl('', [Validators.required]),
    state: new FormControl('', [Validators.required]),
    slug: new FormControl('', [
      Validators.required,
      Validators.pattern('^(?!new$)[a-z0-9-]+$')
    ]),
    image_url: new FormControl('', [Validators.required]),
    synopsis: new FormControl('', [
      Validators.required,
      Validators.maxLength(400)
    ]),
    body: new FormControl('', [Validators.required]),
    is_announcement: new FormControl(false, [Validators.required])
  });

  /** Store authors */
  public authors: PublicProfile[] = [];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private snackBar: MatSnackBar,
    private newsService: NewsService,
    protected formBuilder: FormBuilder
  ) {
    const data = this.route.snapshot.data as {
      article: ArticleOverview | null;
    };
    this.article = data.article;

    /** Set article form data */
    if (this.article) {
      this.articleForm.patchValue(this.article);
    } else {
      this.articleForm.patchValue({
        title: '',
        slug: '',
        image_url: '',
        synopsis: '',
        body: '',
        is_announcement: false
      });
    }
  }

  /** Event handler to handle submitting the the form.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.articleForm.valid) {
      let articleToSubmit = this.article
        ? (this.article! as ArticleDraft)
        : (BLANK_ARTICLE_DRAFT as ArticleDraft);
      Object.assign(articleToSubmit, this.articleForm.value);
      articleToSubmit.authors = this.authors;
      if (this.isNew()) {
        articleToSubmit.published = new Date();
      } else {
        articleToSubmit.last_modified = new Date();
      }
      let submittedArticle = this.isNew()
        ? this.newsService.createArticle(articleToSubmit)
        : this.newsService.updateArticle(articleToSubmit);

      submittedArticle.subscribe({
        next: (article) => this.onSuccess(article),
        error: (err) => this.onError(err)
      });
    }
  }

  /** Opens a confirmation snackbar when an article is successfully updated.
   * @returns {void}
   */
  private onSuccess(article: ArticleOverview): void {
    this.router.navigate(['/article/admin']);
    this.snackBar.open(`Article ${this.action()}`, '', { duration: 2000 });
  }

  /** Opens a snackbar when there is an error updating an article.
   * @returns {void}
   */
  private onError(err: any): void {
    this.snackBar.open(`Error: Article Not ${this.action()}`, '', {
      duration: 2000
    });
  }

  /** Event handler to handle resetting the form.
   * @returns {void}
   */
  onReset() {
    this.articleForm.patchValue(this.article!);
  }

  /** Shorthand for whether the article is new or not.
   * @returns {boolean}
   */
  isNew(): boolean {
    return this.article === null;
  }

  /** Event handler to handle the first change in the article title field
   * Automatically generates a slug from the article title (that can be edited)
   * @returns {void}
   */
  generateSlug(): void {
    const title = this.articleForm.controls['title'].value;
    const slug = this.articleForm.controls['slug'].value;
    if (title && !slug) {
      var generatedSlug = title.toLowerCase().replace(/[^a-zA-Z0-9]/g, '-');
      this.articleForm.setControl('slug', new FormControl(generatedSlug));
    }
  }

  /** Shorthand for determining the action being performed on the organization.
   * @returns {string}
   */
  action(): string {
    return this.isNew() ? 'Created' : 'Updated';
  }
}
