import { Component, signal, WritableSignal } from '@angular/core';
import { MyCoursesService } from '../../my-courses.service';
import {
  CourseSite,
  CourseSiteOverview,
  SectionOverview,
  sectionOverviewToTeachingSectionOverview,
  TeachingSectionOverview,
  TermOverview,
  UpdatedCourseSite
} from '../../my-courses.model';
import { ActivatedRoute } from '@angular/router';
import { FormControl } from '@angular/forms';
import { PublicProfile } from 'src/app/profile/profile.service';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrl: './settings.component.css'
})
export class SettingsComponent {
  [x: string]: any;
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'settings',
    title: 'Course',
    component: SettingsComponent
  };

  /** Stores the course site.  */
  public courseSite: UpdatedCourseSite | null = null;

  /** Section selector */
  title = new FormControl('');
  selectedTerm: FormControl<TermOverview | null> = new FormControl(null);
  selectedSections: WritableSignal<number[]> = signal([]);
  currentSectionInput = signal('');

  /** GTA and UTA selectors */
  public gtas: PublicProfile[] = [];
  public utas: PublicProfile[] = [];

  constructor(
    private route: ActivatedRoute,
    protected myCoursesService: MyCoursesService,
    private snackBar: MatSnackBar
  ) {
    this.resetForm();
  }

  /**
   * Handles the selection of items from the autocomplete dropdown for sections.
   *
   * Logic from the dialog example on the Angular Material docs:
   * https://material.angular.io/components/chips/examples#chips-autocomplete
   */
  selected(event: MatAutocompleteSelectedEvent): void {
    let section = event.option.value as number;
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
  remove(section: SectionOverview | TeachingSectionOverview): void {
    this.selectedSections.update((sections) => {
      let index = sections.indexOf(section.id);
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

  /** Resets the form */
  resetForm() {
    let courseSiteId = this.route.parent!.snapshot.params['course_site_id'];
    this.myCoursesService
      .getCourseSite(courseSiteId)
      .subscribe((courseSite) => {
        this.courseSite = courseSite;
        this.title.setValue(courseSite.title);
        let term = this.myCoursesService
          .allTerms()
          .find((term) => term.id == this.courseSite!.term_id)!;
        this.selectedTerm.setValue(term);
        this.selectedSections.set(this.courseSite.section_ids);
        this.gtas = this.courseSite.gtas;
        this.utas = this.courseSite.utas;
      });
  }

  /** Determines if the form is valid and can be submitted. */
  formIsValid(): boolean {
    return (
      this.title.value !== null &&
      this.title.value !== '' &&
      this.selectedSections().length > 0
    );
  }

  /**
   * Submits the form and creates a new course site.
   */
  submit(): void {
    if (this.courseSite && this.formIsValid()) {
      // Create object
      let updatedCourseSite: UpdatedCourseSite = {
        id: this.courseSite.id,
        title: this.title.value ?? '',
        term_id: this.courseSite.term_id,
        section_ids: this.selectedSections(),
        gtas: this.gtas,
        utas: this.utas
      };

      // Attempt to update
      this.myCoursesService.updateCourseSite(updatedCourseSite).subscribe({
        next: () => {
          this.resetForm();
          this.snackBar.open('Successfully updated the course site.', '', {
            duration: 2000
          });
        },
        error: (err) => {
          this.snackBar.open('Could not save the course site.', '', {
            duration: 2000
          });
        }
      });
    }
  }

  /** Retrieve a section for a given ID */
  sectionForId(id: number) {
    let term = this.myCoursesService
      .allTerms()
      .find((term) => term.id == this.courseSite!.term_id)!;
    console.log(term);
    return (
      term.teaching_no_site.find((section) => section.id === id) ||
      term.sites
        .flatMap((site) => site.sections)
        .find((section) => section.id === id)
    );
  }

  /** Retrieves a list of all sections for the dropwdown */
  allSections() {
    let term = this.myCoursesService
      .allTerms()
      .find((term) => term.id == this.courseSite!.term_id)!;
    return term.teaching_no_site
      .concat(
        term.sites
          .flatMap((site) => site.sections)
          .map(sectionOverviewToTeachingSectionOverview)
      )
      .sort((a, b) => +a.course_number - +b.course_number);
  }
}
