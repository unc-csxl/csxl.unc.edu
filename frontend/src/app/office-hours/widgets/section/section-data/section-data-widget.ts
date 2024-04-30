/**
 * The Section Data widget abstracts the implementation of getting
 * section data away from other components
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import { OfficeHoursService } from '../../../office-hours.service';
import {
  OfficeHoursEventType,
  OfficeHoursSectionTrailingWeekData
} from '../../../office-hours.models';
import { RosterRole } from 'src/app/academics/academics.models';

@Component({
  selector: 'section-data-widget',
  templateUrl: './section-data-widget.html',
  styleUrls: ['./section-data-widget.css']
})
export class SectionData implements OnInit {
  @Input() sectionId!: number;
  data: OfficeHoursSectionTrailingWeekData | null = null;

  constructor(private officeHoursService: OfficeHoursService) {}

  ngOnInit(): void {
    this.getSectionData();
  }

  getSectionData() {
    this.officeHoursService.getSectionData(this.sectionId).subscribe((data) => {
      this.data = data;
    });
  }
}
