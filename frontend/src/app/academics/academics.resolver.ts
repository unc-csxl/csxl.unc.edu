/**
 * The Academics Resolver allows courses data to be injected into the routes
 * of components.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023
 * @license MIT
 */

import { inject } from '@angular/core';
import {
  ActivatedRouteSnapshot,
  ResolveFn,
  RouterStateSnapshot
} from '@angular/router';
import { AcademicsService } from './academics.service';
import { Course, Room, Section, SectionMember, Term } from './academics.models';
import { catchError, of, switchMap } from 'rxjs';

/** This resolver injects the list of courses into the catalog component. */
export const coursesResolver: ResolveFn<Course[] | undefined> = (
  route,
  state
) => {
  return inject(AcademicsService).getCourses();
};

/** This resolver injects the list of courses into the catalog component. */
export const courseResolver: ResolveFn<Course | undefined> = (route, state) => {
  // If the course is new, return a blank one
  if (route.paramMap.get('id')! == 'new') {
    return {
      id: '',
      subject_code: '',
      number: '',
      title: '',
      description: '',
      credit_hours: -1,
      sections: null
    };
  }

  // Otherwise, return the course.
  // If there is an error, return undefined
  return inject(AcademicsService)
    .getCourse(route.paramMap.get('id')!)
    .pipe(
      catchError((error) => {
        console.log(error);
        return of(undefined);
      })
    );
};

/** This resolver injects the list of terms into the offerings component. */
export const termsResolver: ResolveFn<Term[] | undefined> = (route, state) => {
  return inject(AcademicsService).getTerms();
};

/** This resolver injects the current term into the admin component. */
export const currentTermResolver: ResolveFn<Term | undefined> = (
  route,
  state
) => {
  return inject(AcademicsService)
    .getCurrentTerm()
    .pipe(
      catchError((error) => {
        return of(undefined);
      })
    );
};

/** This resolver injects a term into the catalog component. */
export const termResolver: ResolveFn<Term | undefined> = (route, state) => {
  // If the term is new, return a blank one
  if (route.paramMap.get('id')! == 'new') {
    return {
      id: '',
      name: '',
      start: new Date(),
      end: new Date(),
      applications_open: new Date(),
      applications_close: new Date(),
      course_sections: null
    };
  }

  // Otherwise, return the term.
  // If there is an error, return undefined
  return inject(AcademicsService)
    .getTerm(route.paramMap.get('id')!)
    .pipe(
      catchError((error) => {
        console.log(error);
        return of(undefined);
      })
    );
};

/** This resolver injects a section into the catalog component. */
export const sectionResolver: ResolveFn<Section | undefined> = (
  route,
  state
) => {
  // If the term is new, return a blank one
  if (route.paramMap.get('id')! == 'new') {
    return {
      id: null,
      course_id: '',
      number: '',
      term_id: '',
      meeting_pattern: '',
      course: null,
      term: null,
      staff: [],
      lecture_room: null,
      office_hour_rooms: [],
      override_title: '',
      override_description: '',
      enrolled: 0,
      total_seats: 0
    };
  }

  // Otherwise, return the section.
  // If there is an error, return undefined
  return inject(AcademicsService)
    .getSection(+route.paramMap.get('id')!)
    .pipe(
      catchError((error) => {
        console.log(error);
        return of(undefined);
      })
    );
};

export const sectionsResolver: ResolveFn<Section[]> | undefined = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  return inject(AcademicsService).getSectionsByTerm24F();
};

/** This resolver injects the list of rooms into the offerings component. */
export const roomsResolver: ResolveFn<Room[] | undefined> = (route, state) => {
  return inject(AcademicsService).getRooms();
};

/** This resolver injects a room into the catalog component. */
export const roomResolver: ResolveFn<Room | undefined> = (route, state) => {
  // If the term is new, return a blank one
  if (route.paramMap.get('id')! == 'new') {
    return {
      id: '',
      nickname: '',
      building: '',
      room: '',
      capacity: 100,
      reservable: false,
      seats: []
    };
  }

  // Otherwise, return the room.
  // If there is an error, return undefined
  return inject(AcademicsService)
    .getRoom(route.paramMap.get('id')!)
    .pipe(
      catchError((error) => {
        console.log(error);
        return of(undefined);
      })
    );
};
