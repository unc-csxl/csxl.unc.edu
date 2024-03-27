/**
 * The Section Creation Form Component shows options to create a new office hours section and handles the creation.
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
import { OfficeHoursSectionDraft } from '../office-hours.models';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'section-creation-form',
  templateUrl: './section-creation-form.component.html',
  styleUrls: ['./section-creation-form.component.css']
})
export class SectionCreationFormComponent implements OnInit {
  protected academicSections: Section[] = [];

  constructor(
    protected formBuilder: FormBuilder,
    private academicService: AcademicsService,
    private officeHoursService: OfficeHoursService,
    protected snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.getAcademicSections();
  }

  public sectionForm = this.formBuilder.group({
    section_name: '',
    academic_sections: []
  });

  getAcademicSections() {
    // TODO: use the current term instead of F23; Academics service has a method to get the current term
    this.academicService.getTerm('F23').subscribe((term) => {
      this.academicService.getSectionsByTerm(term).subscribe((sections) => {
        this.academicSections = sections;
      });
    });
  }

  onSubmit() {
    if (this.sectionForm.valid) {
      let oh_title = this.sectionForm.value.section_name ?? '';
      let oh_section: OfficeHoursSectionDraft = { title: oh_title };
      let academic_ids = this.sectionForm.value.academic_sections ?? [];
      this.officeHoursService
        .createSection(oh_section, academic_ids)
        .subscribe({
          next: (section) => console.log(section),
          error: (err) => this.onError(err)
        });
    }
  }

  private onError(err: any): void {
    this.snackBar.open('Error: Unable to create Office Hours Section', '', {
      duration: 2000
    });
  }
}
