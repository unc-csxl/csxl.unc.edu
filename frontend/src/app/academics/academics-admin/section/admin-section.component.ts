/**
 * The Sections Admin page enables the administrator to add, edit,
 * and delete sections.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023
 * @license MIT
 */

import { Component, WritableSignal, signal } from '@angular/core';
import { Observable } from 'rxjs';
import { permissionGuard } from 'src/app/permission.guard';
import { CatalogSection, Course, Section, Term } from '../../academics.models';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AcademicsService } from '../../academics.service';
import { FormControl } from '@angular/forms';
import {
  coursesResolver,
  currentTermResolver,
  termsResolver
} from '../../academics.resolver';
import { RxTermList } from '../rx-academics-admin';

@Component({
  selector: 'app-admin-section',
  templateUrl: './admin-section.component.html',
  styleUrls: ['./admin-section.component.css']
})
export class AdminSectionComponent {
  public static Route = {
    path: 'section',
    component: AdminSectionComponent,
    title: 'Section Administration',
    canActivate: [permissionGuard('academics.section', '*')],
    resolve: {
      terms: termsResolver,
      currentTerm: currentTermResolver,
      courses: coursesResolver
    }
  };

  /** Store list of sections */
  public sections: WritableSignal<CatalogSection[]> = signal([]);

  /** Store list of Terms  */
  public terms: RxTermList = new RxTermList();
  public terms$: Observable<Term[]> = this.terms.value$;

  /** Store the currently selected term from the form */
  public displayTerm: FormControl<Term> = new FormControl();

  public displayedColumns: string[] = ['name'];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private snackBar: MatSnackBar,
    private academicsService: AcademicsService
  ) {
    // Initialize data from resolvers
    const data = this.route.snapshot.data as {
      terms: Term[];
      currentTerm: Term | undefined;
    };

    this.terms.set(data.terms);

    if (data.currentTerm) {
      this.displayTerm.setValue(data.currentTerm);

      this.academicsService
        .getSectionsByTerm(data.currentTerm!)
        .subscribe((sections) => {
          this.sections.set(sections);
        });
    }
  }

  /** Event handler to open the Section Editor to create a new term */
  createSection(): void {
    // Navigate to the section editor
    this.router.navigate(['academics', 'section', 'edit', 'new']);
  }

  /** Event handler to open the Section Editor to update a section
   * @param section: section to update
   */
  updateSection(section: Section): void {
    // Navigate to the section editor
    this.router.navigate(['academics', 'section', 'edit', section.id]);
  }

  /** Delete a section object from the backend database table using the backend HTTP delete request.
   * @param section: section to delete
   * @param event: event to stop progagation
   * @returns void
   */
  deleteSection(section: Section, event: Event): void {
    event.stopPropagation();
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this section?',
      'Delete'
    );
    confirmDelete.onAction().subscribe(() => {
      this.academicsService.deleteSection(section).subscribe(() => {
        let termToUpdate = this.displayTerm.value;
        this.sections.update((sections) =>
          sections.filter((s) => s.id !== section.id)
        );
        this.terms.updateTerm(termToUpdate);
        this.snackBar.open('This Section has been deleted.', '', {
          duration: 2000
        });
      });
    });
  }
}
