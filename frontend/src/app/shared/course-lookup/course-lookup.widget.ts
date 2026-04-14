/**
 * The Course Lookup Widget allows users to search for a course
 * from a preloaded list.
 */

import {
  Component,
  ElementRef,
  EventEmitter,
  Input,
  Output,
  ViewChild
} from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { Observable, map, startWith } from 'rxjs';
import { Course } from 'src/app/academics/academics.models';

@Component({
  selector: 'course-lookup',
  templateUrl: './course-lookup.widget.html',
  styleUrls: ['./course-lookup.widget.css'],
  standalone: false
})
export class CourseLookup {
  @Input() label: string = 'Course';
  @Input() courses: Course[] = [];
  @Input() disabled: boolean | null = false;

  private _selectedCourse: Course | null = null;

  @Input() set selectedCourse(course: Course | null) {
    this._selectedCourse = course;
    if (!course) {
      this.courseLookup.setValue('', { emitEvent: false });
    }
  }

  get selectedCourse(): Course | null {
    return this._selectedCourse;
  }

  @Output() selectedCourseChange: EventEmitter<Course | null> =
    new EventEmitter();

  public courseLookup = new FormControl<string | Course>('');
  public filteredCourses$: Observable<Course[]> =
    this.courseLookup.valueChanges.pipe(
      startWith(''),
      map((value) => {
        const courses = this.filterCourses(this.displayCourse(value));
        this.filteredCourses = courses;
        return courses;
      })
    );

  @ViewChild('courseInput') courseInput?: ElementRef<HTMLInputElement>;
  private filteredCourses: Course[] = [];

  onCourseAdded(event: MatAutocompleteSelectedEvent): void {
    const course = event.option.value as Course;
    this.selectCourse(course);
  }

  onCourseRemoved(): void {
    this.clearLookup();
    this.selectedCourseChange.emit(null);
  }

  displayCourse = (course: Course | string | null): string => {
    if (!course) {
      return '';
    }

    if (typeof course === 'string') {
      return course;
    }

    return `${course.subject_code} ${course.number}: ${course.title}`;
  };

  onLookupKeydown(event: Event): void {
    if (this.filteredCourses.length === 1) {
      event.preventDefault();
      this.selectCourse(this.filteredCourses[0]);
    }
  }

  private clearLookup(): void {
    if (this.courseInput) {
      this.courseInput.nativeElement.value = '';
    }

    this.courseLookup.setValue('', { emitEvent: false });
  }

  private selectCourse(course: Course): void {
    this.clearLookup();
    this.selectedCourseChange.emit(course);
  }

  private filterCourses(search: string): Course[] {
    const normalizedSearch = search.trim().toLowerCase();
    const selectableCourses = this.courses.filter(
      (course) => course.id !== this.selectedCourse?.id
    );

    if (!normalizedSearch) {
      return selectableCourses;
    }

    return selectableCourses.filter((course) =>
      [course.subject_code, course.number, course.title]
        .filter(Boolean)
        .join(' ')
        .toLowerCase()
        .includes(normalizedSearch)
    );
  }
}
