import {
  Component,
  Inject,
  Signal,
  WritableSignal,
  signal
} from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import {
  NewCourseSite,
  TeachingSectionOverview,
  TermOverview
} from '../../my-courses.model';
import { MyCoursesService } from '../../my-courses.service';
import { Router } from '@angular/router';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatChipInputEvent } from '@angular/material/chips';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'dialog-create-course-site',
  templateUrl: './create-course-site.dialog.html',
  styleUrl: './create-course-site.dialog.css'
})
export class CreateCourseSiteDialog {
  /** Course Site Form */

  title = new FormControl('');
  selectedTerm: FormControl<TermOverview | null>;
  selectedSections: WritableSignal<TeachingSectionOverview[]> = signal([]);
  currentSectionInput = signal('');

  constructor(
    protected dialogRef: MatDialogRef<CreateCourseSiteDialog>,
    @Inject(MAT_DIALOG_DATA) public data: TermOverview[],
    protected myCoursesService: MyCoursesService,
    private router: Router,
    private snackBar: MatSnackBar,
    protected formBuilder: FormBuilder
  ) {
    this.selectedTerm = new FormControl(myCoursesService.allTerms()[0]);
  }

  /**
   * Handles the selection of items from the autocomplete dropdown for sections.
   *
   * Logic from the dialog example on the Angular Material docs:
   * https://material.angular.io/components/chips/examples#chips-autocomplete
   */
  selected(event: MatAutocompleteSelectedEvent): void {
    let section = event.option.value as TeachingSectionOverview;
    this.selectedSections.update((sections) => [...sections, section]);
    this.currentSectionInput.set('');
    event.option.deselect();
  }

  /**
   * Handles the removal of items from the autocomplete dropdown for sections.
   *
   * Logic from the dialog example on the Angular Material docs:
   * https://material.angular.io/components/chips/examples#chips-autocomplete
   */
  remove(setion: TeachingSectionOverview): void {
    this.selectedSections.update((sections) => {
      let index = sections.indexOf(setion);
      if (index < 0) {
        return sections;
      }

      sections.splice(index, 1);
      return [...sections];
    });
  }

  /** Resets the sections back to an empty list. */
  resetSections(): void {
    this.selectedSections.set([]);
  }

  /** Determines if the form is valid and can be submitted. */
  formIsValid(): boolean {
    return (
      this.title.value !== null &&
      this.title.value !== '' &&
      this.selectedTerm.value !== null &&
      this.selectedSections().length > 0
    );
  }

  /**
   * Submits the form and creates a new course site.
   */
  submit(): void {
    if (this.formIsValid()) {
      // Create the new course site object
      let newCourseSite: NewCourseSite = {
        title: this.title.value ?? '',
        term_id: this.selectedTerm.value!.id,
        section_ids: this.selectedSections()!.map((section) => section.id)
      };

      // Attempt to create the course site
      this.myCoursesService.createCourseSite(newCourseSite).subscribe({
        next: (courseSite) => {
          // Reset the service's term overview data
          this.myCoursesService.getTermOverviews();
          // Navigate to the newly created course site
          this.router.navigate(['course', courseSite.id, 'office-hours']);
          // Close the dialog
          this.close();
        },
        error: (err) => this.snackBar.open(err, '', { duration: 2000 })
      });
    }
  }

  /** Closes the dialog */
  close(): void {
    this.dialogRef.close();
  }
}
