/**
 * The Term editor page enables the administrator to add and edit
 * terms.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023
 * @license MIT
 */

import { Component, inject } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  CanActivateFn,
  Route,
  Router,
  RouterStateSnapshot
} from '@angular/router';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { PermissionService } from 'src/app/permission.service';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { termResolver } from 'src/app/academics/academics.resolver';
import { Term } from 'src/app/academics/academics.models';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AcademicsService } from 'src/app/academics/academics.service';
import { Profile } from 'src/app/models.module';
import { DatePipe } from '@angular/common';

const canActivateEditor: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  /** Determine if page is viewable by user based on permissions */

  let id: string = route.params['id'];

  if (id === 'new') {
    return inject(PermissionService).check('academics.term.create', 'term');
  } else {
    return inject(PermissionService).check(
      'academics.term.update',
      `term/${id}`
    );
  }
};
@Component({
  selector: 'app-term-editor',
  templateUrl: './term-editor.component.html',
  styleUrls: ['./term-editor.component.css']
})
export class TermEditorComponent {
  /** Route information to be used in the Routing Module */
  public static Route: Route = {
    path: 'term/edit/:id',
    component: TermEditorComponent,
    title: 'Term Editor',
    canActivate: [canActivateEditor],
    resolve: {
      profile: profileResolver,
      term: termResolver
    }
  };

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile | null = null;

  /** Store the term.  */
  public term: Term;

  /** Store the term id. */
  termId: string = 'new';

  /** Add validators to the form */
  id = new FormControl('', [Validators.required]);
  name = new FormControl('', [Validators.required]);
  start = new FormControl('', [Validators.required]);
  end = new FormControl('', [Validators.required]);
  applications_open = new FormControl('', [Validators.required]);
  applications_close = new FormControl('', [Validators.required]);

  /** Term Editor Form */
  public termForm = this.formBuilder.group({
    id: this.id,
    name: this.name,
    start: this.start,
    end: this.end,
    applications_open: this.applications_open,
    applications_close: this.applications_close
  });

  /** Constructs the term editor component */
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar,
    private academicsService: AcademicsService,
    private datePipe: DatePipe
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      profile: Profile;
      term: Term;
    };
    this.profile = data.profile;
    this.term = data.term;

    console.log(data.term);

    /** Get id from the url */
    this.termId = this.route.snapshot.params['id'];

    /** Set term form data */
    this.termForm.setValue({
      id: this.termId == 'new' ? '' : this.term.id,
      name: this.term.name,
      start: this.datePipe.transform(this.term.start, 'yyyy-MM-ddTHH:mm'),
      end: this.datePipe.transform(this.term.end, 'yyyy-MM-ddTHH:mm'),
      applications_open: this.datePipe.transform(
        this.term.applications_open,
        'yyyy-MM-ddTHH:mm'
      ),
      applications_close: this.datePipe.transform(
        this.term.applications_close,
        'yyyy-MM-ddTHH:mm'
      )
    });
  }

  /** Event handler to handle submitting the Update Term Form.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.termForm.valid) {
      Object.assign(this.term, this.termForm.value);

      if (this.termId == 'new') {
        this.academicsService.createTerm(this.term).subscribe({
          next: (term) => this.onSuccess(term),
          error: (err) => this.onError(err)
        });
      } else {
        this.academicsService.updateTerm(this.term).subscribe({
          next: (term) => this.onSuccess(term),
          error: (err) => this.onError(err)
        });
      }
    }
  }

  /** Opens a confirmation snackbar when a course is successfully updated.
   * @returns {void}
   */
  private onSuccess(term: Term): void {
    this.router.navigate(['/academics/admin/term']);

    let message: string =
      this.termId === 'new' ? 'Term Created' : 'Term Updated';

    this.snackBar.open(message, '', { duration: 2000 });
  }

  /** Opens a snackbar when there is an error updating a course.
   * @returns {void}
   */
  private onError(err: any): void {
    let message: string =
      this.termId === 'new'
        ? 'Error: Course Not Created'
        : 'Error: Course Not Updated';

    this.snackBar.open(message, '', {
      duration: 2000
    });
  }
}
