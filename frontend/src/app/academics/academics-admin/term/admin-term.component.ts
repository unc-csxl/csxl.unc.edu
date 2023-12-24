import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { permissionGuard } from 'src/app/permission.guard';
import { Term } from '../../academics.models';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AcademicsService } from '../../academics.service';

@Component({
  selector: 'app-admin-term',
  templateUrl: './admin-term.component.html',
  styleUrls: ['./admin-term.component.css']
})
export class AdminTermComponent {
  public static Route = {
    path: 'term',
    component: AdminTermComponent,
    title: 'Term Administration',
    canActivate: [permissionGuard('academics.term', '*')]
  };

  /** Terms List */
  public terms$: Observable<Term[]>;

  public displayedColumns: string[] = ['name'];

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private academicsService: AcademicsService
  ) {
    this.terms$ = academicsService.getTerms();
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
   * @returns void
   */
  deleteTerm(term: Term): void {
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this term?',
      'Delete'
    );
    confirmDelete.onAction().subscribe(() => {
      this.academicsService.deleteTerm(term).subscribe(() => {
        this.snackBar.open('This term has been deleted.', '', {
          duration: 2000
        });
      });
    });
  }
}
