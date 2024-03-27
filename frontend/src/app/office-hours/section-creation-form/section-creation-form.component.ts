import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Section, Term } from 'src/app/academics/academics.models';
import { AcademicsService } from 'src/app/academics/academics.service';
import { OfficeHoursService } from '../office-hours.service';
import { OfficeHoursSectionDraft } from '../office-hours.models';

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
    private officeHoursService: OfficeHoursService
  ) {}

  ngOnInit(): void {
    this.getAcademicSections();
  }

  public sectionForm = this.formBuilder.group({
    section_name: '',
    academic_sections: []
  });

  getAcademicSections() {
    this.academicService.getTerm('F23').subscribe((term) => {
      this.academicService.getSectionsByTerm(term).subscribe((sections) => {
        this.academicSections = sections;
      });
    });
  }

  onSubmit() {
    if (this.sectionForm.valid) {
      let oh_title = this.sectionForm.value.section_name ?? '';
      let section_draft: OfficeHoursSectionDraft = { title: oh_title };
      let academic_ids = this.sectionForm.value.academic_sections ?? [];
      console.log(oh_title);
      console.log(section_draft);
      console.log(academic_ids);
      this.officeHoursService
        .createSection(section_draft, academic_ids)
        .subscribe({
          next: (section) => console.log(section)
        });
    }
  }
}
function OfficeHoursSectionDraft(title: string) {
  throw new Error('Function not implemented.');
}
