/**
 * The Course editor page enables the administrator to add and edit
 * courses.
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
import { courseResolver } from 'src/app/academics/academics.resolver';
import { Course } from 'src/app/academics/academics.models';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AcademicsService } from 'src/app/academics/academics.service';
import { Profile } from 'src/app/models.module';

const canActivateEditor: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  /** Determine if page is viewable by user based on permissions */

  let id: string = route.params['id'];

  if (id === 'new') {
    return inject(PermissionService).check('academics.course.create', 'course');
  } else {
    return inject(PermissionService).check(
      'academics.course.update',
      `course/${id}`
    );
  }
};

@Component({
  selector: 'app-course-editor',
  templateUrl: './course-editor.component.html',
  styleUrls: ['./course-editor.component.css']
})
export class CourseEditorComponent {
  /** Route information to be used in the Routing Module */
  public static Route: Route = {
    path: 'course/edit/:id',
    component: CourseEditorComponent,
    title: 'Course Editor',
    canActivate: [canActivateEditor],
    resolve: {
      profile: profileResolver,
      course: courseResolver
    }
  };

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile | null = null;

  /** Store the course.  */
  public course: Course;

  /** Store the course id. */
  courseId: string = 'new';

  /** Add validators to the form */
  subject_code = new FormControl('', [Validators.required]);
  number = new FormControl('', [Validators.required]);
  title = new FormControl('', [Validators.required]);
  description = new FormControl('', [Validators.required]);
  credit_hours = new FormControl(3, [Validators.required]);

  /** Course Editor Form */
  public courseForm = this.formBuilder.group({
    subject_code: this.subject_code,
    number: this.number,
    title: this.title,
    description: this.description,
    credit_hours: this.credit_hours
  });

  /** Constructs the course editor component */
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar,
    private academicsService: AcademicsService
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      profile: Profile;
      course: Course;
    };
    this.profile = data.profile;
    this.course = data.course;

    /** Set course form data */
    this.courseForm.setValue({
      subject_code: this.course.subject_code,
      number: this.course.number,
      title: this.course.title,
      description: this.course.description,
      credit_hours: this.course.credit_hours
    });

    /** Get id from the url */
    this.courseId = this.route.snapshot.params['id'];
  }

  /** Event handler to handle submitting the Update Course Form.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.courseForm.valid) {
      Object.assign(this.course, this.courseForm.value);
      this.course.id =
        this.course.subject_code.toLowerCase() + this.course.number;

      if (this.courseId == 'new') {
        this.academicsService.createCourse(this.course).subscribe({
          next: (course) => this.onSuccess(course),
          error: (err) => this.onError(err)
        });
      } else {
        this.academicsService.updateCourse(this.course).subscribe({
          next: (course) => this.onSuccess(course),
          error: (err) => this.onError(err)
        });
      }
    }
  }

  /** Opens a confirmation snackbar when a course is successfully updated.
   * @returns {void}
   */
  private onSuccess(course: Course): void {
    this.router.navigate(['/academics/admin/']);

    let message: string =
      this.courseId === 'new' ? 'Course Created' : 'Course Updated';

    this.snackBar.open(message, '', { duration: 2000 });
  }

  /** Opens a snackbar when there is an error updating a course.
   * @returns {void}
   */
  private onError(err: any): void {
    let message: string =
      this.courseId === 'new'
        ? 'Error: Course Not Created'
        : 'Error: Course Not Updated';

    this.snackBar.open(message, '', {
      duration: 2000
    });
  }
}
