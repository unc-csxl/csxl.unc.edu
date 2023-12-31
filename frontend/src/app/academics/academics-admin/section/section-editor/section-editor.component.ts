/**
 * The Section editor page enables the administrator to add and edit
 * sections.
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
import {
  coursesResolver,
  roomsResolver,
  sectionResolver,
  termResolver,
  termsResolver
} from 'src/app/academics/academics.resolver';
import {
  Course,
  Room,
  Section,
  Term
} from 'src/app/academics/academics.models';
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
    return inject(PermissionService).check(
      'academics.section.create',
      'section'
    );
  } else {
    return inject(PermissionService).check(
      'academics.section.update',
      `section/${id}`
    );
  }
};
@Component({
  selector: 'app-section-editor',
  templateUrl: './section-editor.component.html',
  styleUrls: ['./section-editor.component.css']
})
export class SectionEditorComponent {
  /** Route information to be used in the Routing Module */
  public static Route: Route = {
    path: 'section/edit/:id',
    component: SectionEditorComponent,
    title: 'Section Editor',
    canActivate: [canActivateEditor],
    resolve: {
      profile: profileResolver,
      section: sectionResolver,
      terms: termsResolver,
      courses: coursesResolver,
      rooms: roomsResolver
    }
  };

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile | null = null;

  /** Store the section.  */
  public section: Section;

  /** Store a list of terms. */
  public terms: Term[];

  /** Store a list of courses. */
  public courses: Course[];

  /** Store a list of rooms. */
  public rooms: Room[];

  /** Store the section id. */
  sectionIdString: string = 'new';

  /** Add validators to the form */
  public term: FormControl<Term | null> = new FormControl(null, [
    Validators.required
  ]);
  public course: FormControl<Course | null> = new FormControl(null, [
    Validators.required
  ]);
  number = new FormControl('', [Validators.required]);
  meeting_pattern = new FormControl('', [Validators.required]);
  public room: FormControl<Room | null> = new FormControl(null, [
    Validators.required
  ]);

  /** Section Editor Form */
  public sectionForm = this.formBuilder.group({
    number: this.number,
    meeting_pattern: this.meeting_pattern
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
      section: Section;
      terms: Term[];
      courses: Course[];
      rooms: Room[];
    };

    this.profile = data.profile;
    this.section = data.section;
    this.terms = data.terms;
    this.courses = data.courses;
    this.rooms = data.rooms;

    /** Get id from the url */
    this.sectionIdString = this.route.snapshot.params['id'];

    /** Set section form data */
    this.sectionForm.setValue({
      number: this.section.number,
      meeting_pattern: this.section.meeting_pattern
    });
    /** Select the term, course, and room, if it exists. */
    let termFilter = this.terms.filter((t) => t.id == this.section.term_id);
    let courseFilter = this.courses.filter(
      (c) => c.id == this.section.course_id
    );
    let roomFilter = this.rooms.filter(
      (c) => c.id == this.section.lecture_room?.id
    );
    this.term.setValue(termFilter.length > 0 ? termFilter[0] : null);
    this.course.setValue(courseFilter.length > 0 ? courseFilter[0] : null);
    this.room.setValue(roomFilter.length > 0 ? roomFilter[0] : null);
  }

  /** Event handler to handle submitting the Update Section Form.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.sectionForm.valid) {
      this.section.id = +this.sectionIdString;
      this.section.number = this.sectionForm.value.number ?? '';
      this.section.meeting_pattern =
        this.sectionForm.value.meeting_pattern ?? '';
      this.section.term_id = this.term.value!.id;
      this.section.course_id = this.course.value!.id;

      this.section.lecture_room = this.room.value!;

      if (this.sectionIdString == 'new') {
        this.academicsService.createSection(this.section).subscribe({
          next: (section) => this.onSuccess(section),
          error: (err) => this.onError(err)
        });
      } else {
        this.academicsService.updateSection(this.section).subscribe({
          next: (section) => this.onSuccess(section),
          error: (err) => this.onError(err)
        });
      }
    }
  }

  /** Opens a confirmation snackbar when a course is successfully updated.
   * @returns {void}
   */
  private onSuccess(section: Section): void {
    this.router.navigate(['/academics/admin/section']);

    let message: string =
      this.sectionIdString === 'new' ? 'Section Created' : 'Section Updated';

    this.snackBar.open(message, '', { duration: 2000 });
  }

  /** Opens a snackbar when there is an error updating a course.
   * @returns {void}
   */
  private onError(err: any): void {
    let message: string =
      this.sectionIdString === 'new'
        ? 'Error: Section Not Created'
        : 'Error: Section Not Updated';

    this.snackBar.open(message, '', {
      duration: 2000
    });
  }
}
