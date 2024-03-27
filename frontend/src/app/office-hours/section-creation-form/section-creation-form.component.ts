import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Section, Term } from 'src/app/academics/academics.models';
import { AcademicsService } from 'src/app/academics/academics.service';

@Component({
  selector: 'section-creation-form',
  templateUrl: './section-creation-form.component.html',
  styleUrls: ['./section-creation-form.component.css']
})
export class SectionCreationFormComponent implements OnInit {
  protected academicSections: Section[] = [];

  constructor(
    protected formBuilder: FormBuilder,
    private academicService: AcademicsService
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

  onSubmit() {}
}
