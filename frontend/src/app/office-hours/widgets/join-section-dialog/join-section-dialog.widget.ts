import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { AcademicsService } from 'src/app/academics/academics.service';
import { OfficeHoursService } from '../../office-hours.service';
import {
  OfficeHoursSection,
  OfficeHoursSectionDetails,
  OfficeHoursSectionPartial
} from '../../office-hours.models';

@Component({
  selector: 'join-section-dialog',
  templateUrl: './join-section-dialog.widget.html',
  styleUrls: ['./join-section-dialog.widget.css']
})
export class JoinSectionDialog implements OnInit {
  protected officeHoursSections: OfficeHoursSection[] = [];

  constructor(
    public dialogRef: MatDialogRef<JoinSectionDialog>,
    protected formBuilder: FormBuilder,
    private academicsService: AcademicsService,
    private officeHoursService: OfficeHoursService
  ) {}

  ngOnInit(): void {
    this.getOfficeHoursSection();
  }

  public joinSectionForm = this.formBuilder.group({
    oh_section: []
  });

  onNoClick(): void {
    this.dialogRef.close();
  }

  getOfficeHoursSection() {
    // TODO: change 'F23' to the current term using the academics service (this has a method to get current term)
    this.officeHoursService
      .getSectionsByTerm('F23')
      .subscribe((oh_sections) => {
        this.officeHoursSections = oh_sections;
      });
  }

  onSubmit() {
    console.log(this.joinSectionForm.value.oh_section);
    if (this.joinSectionForm.valid) {
      let oh_sections: OfficeHoursSectionDetails[] =
        this.joinSectionForm.value.oh_section ?? [];
      console.log(oh_sections);
      console.log(oh_sections[0]);
      this.officeHoursService.joinSection(oh_sections).subscribe({
        next: (section_member) => console.log(section_member)
      });
    }
  }
}
