import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { permissionGuard } from 'src/app/permission.guard';
import { Course, Section, Term } from '../../academics.models';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AcademicsService } from '../../academics.service';
import { FormControl } from '@angular/forms';
import { coursesResolver, termsResolver } from '../../academics.resolver';

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
    resolve: { terms: termsResolver, courses: coursesResolver }
  };

  /** Store list of sections */
  public sections$: Observable<Section[]>;

  /** Store list of Terms  */
  public terms: Term[];

  /** Store list of Courses  */
  public courses: Course[];

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
      courses: Course[];
    };
    this.terms = data.terms;
    this.courses = data.courses;

    this.displayTerm.setValue(this.terms[1]);

    this.sections$ = academicsService.getSectionsByTerm(this.displayTerm.value);
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
    this.router.navigate(['academics', 'term', 'edit', section.id]);
  }

  /** Delete a section object from the backend database table using the backend HTTP delete request.
   * @param section: section to delete
   * @returns void
   */
  deleteSection(section: Section): void {
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this section?',
      'Delete'
    );
    confirmDelete.onAction().subscribe(() => {
      this.academicsService.deleteSection(section).subscribe(() => {
        this.snackBar.open('This term has been deleted.', '', {
          duration: 2000
        });
      });
    });
  }

  /** Helper function that returns the course object from the list with the given ID.
   * @param id ID of the course to look up.
   * @returns Course for the ID, if it exists.
   */
  courseFromId(id: string): Course | null {
    // Find the course for the given ID
    let coursesFilter = this.courses.filter((c) => c.id === id);
    // Return either the course if it exists, or null.
    return coursesFilter.length > 0 ? coursesFilter[0] : null;
  }
}
