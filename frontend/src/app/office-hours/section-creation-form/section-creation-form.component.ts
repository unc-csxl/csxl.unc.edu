/**
 * The Section Creation Form Component allows TAs to create a new Office Hours section
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Section } from 'src/app/academics/academics.models';
import { AcademicsService } from 'src/app/academics/academics.service';
import { OfficeHoursService } from '../office-hours.service';
import {
  OfficeHoursSectionDetails,
  OfficeHoursSectionDraft
} from '../office-hours.models';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'section-creation-form',
  templateUrl: './section-creation-form.component.html',
  styleUrls: ['./section-creation-form.component.css']
})
export class SectionCreationFormComponent implements OnInit {
  /* List of all academic sections within the current term */
  protected academicSections: Section[] = [];

  constructor(
    protected formBuilder: FormBuilder,
    private academicService: AcademicsService,
    private officeHoursService: OfficeHoursService,
    protected snackBar: MatSnackBar
  ) {}

  /* On initialization, get all academic sections */
  ngOnInit(): void {
    this.getAcademicSections();
  }

  public sectionForm = this.formBuilder.group({
    section_name: '',
    academic_sections: []
  });

  /* Gets all academic sections in the current academic term */
  //TODO: use current term instead of 'F23'
  getAcademicSections() {
    this.academicService.getCurrentTerm().subscribe((term) => {
      this.academicService
        .getSectionsWithNoOfficeHoursByTerm(term)
        .subscribe((sections) => {
          this.academicSections = sections;
        });
    });
  }

  onSubmit() {
    // If section creation form is valid, create new office hours section linked to academic section(s)
    if (this.sectionForm.valid) {
      let oh_title = this.sectionForm.value.section_name ?? '';
      let oh_section: OfficeHoursSectionDraft = { title: oh_title };
      let academic_ids = this.sectionForm.value.academic_sections ?? [];
      this.officeHoursService
        .createSection(oh_section, academic_ids)
        .subscribe({
          next: (section) => this.onSuccess(section),
          error: (err) => this.onError(err)
        });
    }
  }

  private onError(err: any): void {
    this.snackBar.open('Error: Unable to create Office Hours Section', '', {
      duration: 2000
    });
  }

  private onSuccess(section: OfficeHoursSectionDetails): void {
    this.snackBar.open('New Office Hours Section Has Been Created!', '', {
      duration: 4000
    });
    this.sectionForm.reset();
  }
}
