/**
 * The Term Admin page enables the administrator to add, edit,
 * and delete terms.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023
 * @license MIT
 */

import { Component, WritableSignal, signal } from '@angular/core';
import { Observable } from 'rxjs';
import { permissionGuard } from 'src/app/permission.guard';
import { Term } from '../../academics.models';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AcademicsService } from '../../academics.service';
import { RxTermList } from '../rx-academics-admin';

@Component({
  selector: 'app-admin-term',
  templateUrl: './admin-term.component.html',
  standalone: false
})
export class AdminTermComponent {
  public static Route = {
    path: 'term',
    component: AdminTermComponent,
    title: 'Term Administration',
    canActivate: [permissionGuard('academics.term', '*')]
  };

  /** Terms List */
  terms: WritableSignal<Term[]> = signal([]);

  public displayedColumns: string[] = ['name'];

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private academicsService: AcademicsService
  ) {
    academicsService.getTerms().subscribe((terms) => {
      this.terms.set(terms);
    });
  }

  /** Event handler to open the Term Editor to create a new term */
  createTerm(): void {
    // Navigate to the term editor
    this.router.navigate(['academics', 'term', 'edit', 'new']);
  }

  /** Event handler to open the Term Editor to update a course
   * @param term: term to update
   */
  updateTerm(term: Term): void {
    // Navigate to the course editor
    this.router.navigate(['academics', 'term', 'edit', term.id]);
  }

  /** Delete a temr object from the backend database table using the backend HTTP delete request.
   * @param term: term to delete
   * @param event: event to stop progagation
   * @returns void
   */
  deleteTerm(term: Term, event: Event): void {
    event.stopPropagation();
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this term?',
      'Delete'
    );
    confirmDelete.onAction().subscribe(() => {
      this.academicsService.deleteTerm(term).subscribe(() => {
        this.terms.update((terms) => {
          let newTerms = terms.filter((t) => t.id !== term.id);
          return [...newTerms];
        });
        this.snackBar.open('This term has been deleted.', '', {
          duration: 2000
        });
      });
    });
  }
}
