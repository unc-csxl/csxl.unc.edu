import { RxObject } from 'src/app/rx-object';
import { Course, Section, Term } from '../academics.models';

export class RxTermList extends RxObject<Term[]> {
  pushTerm(term: Term): void {
    this.value.push(term);
    this.notify();
  }

  updateTerm(term: Term): void {
    this.value = this.value.map((o) => {
      return o.id !== term.id ? o : term;
    });
    this.notify();
  }

  removeTerm(termToRemove: Term): void {
    this.value = this.value.filter((term) => termToRemove.id !== term.id);
    this.notify();
  }
}

export class RxCourseList extends RxObject<Course[]> {
  pushCourse(course: Course): void {
    this.value.push(course);
    this.notify();
  }

  updateCourse(course: Course): void {
    this.value = this.value.map((o) => {
      return o.id !== course.id ? o : course;
    });
    this.notify();
  }

  removeCourse(courseToRemove: Course): void {
    this.value = this.value.filter((course) => courseToRemove.id !== course.id);
    this.notify();
  }
}

export class RxSectionList extends RxObject<Section[]> {
  pushSection(section: Section): void {
    this.value.push(section);
    this.notify();
  }

  updateSection(section: Section): void {
    this.value = this.value.map((o) => {
      return o.id !== section.id ? o : section;
    });
    this.notify();
  }

  removeSection(sectionToRemove: Section): void {
    this.value = this.value.filter(
      (section) => sectionToRemove.id !== section.id
    );
    this.notify();
  }
}
